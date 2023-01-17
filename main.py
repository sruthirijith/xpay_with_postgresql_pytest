import shutil
from fastapi import FastAPI, Depends, UploadFile
from sqlalchemy.orm import Session
from security.jwt_handler import signJWT_access, signJWT_refresh, decodeJWT
from security.jwt_bearer import JWTBearer
from database import engine, Base, get_db
import models
import schema
import crud

Base.metadata.create_all(bind=engine)
app= FastAPI(title="User_Registration")


@app.post('/xpay_user_creation')
async def user_register(data:schema.Base, user_db:Session=Depends(get_db)):
    """user registration"""
    receive_data = user_db.query(models.xpay_user).filter(models.xpay_user.mobile_no==data.mobile_no).first()
    if receive_data:
        return {'message':'phone number already in db'}
    receive_data1 = user_db.query(models.xpay_user).filter(models.xpay_user.email==data.email).first()
    if receive_data1:
        return {'message':' email already in db'}
    user_details = models.xpay_user(**data.dict())
    user_db.add( user_details)
    user_db.commit()
    receive_data2 = user_db.query(models.xpay_user.id).filter(models.xpay_user.mobile_no==data.mobile_no).first()
    return {'message':'registered succesfully'}
@app.post('/employee login')
def employee_login(data:schema.login,user_db:Session=Depends(get_db)):
    """login a user by email and password"""
    login_data=user_db.query(models.xpay_user).filter(models.xpay_user.email==data.email, models.xpay_user.password==data.password).first()
    if login_data:
        access_token=signJWT_access(login_data.mobile_no)
        refresh_token=signJWT_refresh(login_data.mobile_no)
        #return {"message":"login succesfull","access_token":access_token,"refresh_token":refresh_token}
        return {"message":"login succesfull"}
    return {"message":"invalid username/password"}  
@app.post("/profile creation", tags=["profile"])   
async def profile_creation(data:schema.Profile,
                           user_db:Session = Depends(get_db),
                           token:str=Depends(JWTBearer())):
    """profile creation """                       
    decodedata= decodeJWT(token)
    users = crud.get_user_by_phone(user_db,mobile_no=decodedata['mobile_number'])
    if users:
        profile_id = user_db.query(models.xpay_profile).filter(models.xpay_profile.user_id==users.id).first()
        if profile_id:
            return {"message":"profile already exist"}
        
        profile_details=models.xpay_profile(first_name=data.first_name,
                                        last_name = data.last_name,
                                        city = data.city,
                                        place_of_birth= data.place_of_birth,
                                        user_id=users.id)
        user_db.add(profile_details)
        user_db.commit()                            
        return {"message":"profile added succesfully" }   
@app.put("/image creation", tags=["profile"])
async def image_upload(image: UploadFile,user_db:Session = Depends(get_db),token:str=Depends(JWTBearer())):
     decodedata= decodeJWT(token)
     users = crud.get_user_by_phone(user_db,mobile_no=decodedata['mobile_number'])
     if users:
        profile_id = user_db.query(models.xpay_profile).filter(models.xpay_profile.user_id==users.id).first()
        if profile_id:
            file_path = f"profile_img/{image.filename}"
            with open(file_path,"wb") as buffer:
                shutil.copyfileobj(image.file,buffer)
            profile_id.image=file_path
            user_db.add(profile_id)
            user_db.commit()         
            user_db.refresh(profile_id)                   
            return {"message":"image added succesfully" }   
