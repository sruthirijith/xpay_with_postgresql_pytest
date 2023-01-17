from starlette.testclient import TestClient

from main import app

client = TestClient(app)



def test_user_creation():
    data ={   "username":"suresh",  
              "email" :"suresh@gmail.com", 
              "mobile_no":"9746298489", 
            "password" :"suresh1992"     
           }
    response = client.post("/xpay_user_creation",json=data)
    assert response.status_code ==200
    assert response.json() ==  {'message':'registered succesfully'}
    
    data ={   "username":"sruthi1",  
              "email" :"sruthi@gmail1.com", 
              "mobile_no":"9746238486", 
            "password" :"sruthi19921"     
           }
    response = client.post("/xpay_user_creation",json=data)
    assert response.status_code ==200
    assert response.json() == {'message':'phone number already in db'}
                            
    data ={   "username":"sruthi3",  
              "email" :"sruthi@gmail.com", 
              "mobile_no":"9746238488", 
            "password" :"sruthi19924"     
           }
    response = client.post("/xpay_user_creation",json=data)
    assert response.status_code ==200
    assert response.json() == {'message':' email already in db'}
 
def test_user_login():
        data= { "email":"sruthi@gmail.com",
          "password":"sruthi1992"}
        response =  client.post('/employee login', json=data)   
        assert response.status_code == 200
        assert response.json() == {"message":"login succesfull"}

        data= { "email":"sruthi1@gmail.com",
          "password":"sruthi1995"}
        response =  client.post('/employee login', json=data)   
        assert response.status_code == 200
        assert response.json() ==  {"message":"invalid username/password"}  

def test_user_profile():
    data = {"first_name":"sruthi",
            "last_name" :"rijith",
            "city" : "kochi",
            "place_of_birth" :"kannur",
            "user_id"  : "1"
      }
    response = client.post('/profile creation', json=data)
    assert response.status_code ==200
    assert response.json()==  {"message":"profile already exist"}

    data = {"first_name":"greeshma",
            "last_name" :"sreerag",
            "city" : "canada",
            "place_of_birth" :"kannur"
      }
    response = client.post('/profile creation', json=data)
    assert response.status_code ==200
    assert response.json()==   {"message":"profile added succesfully" } 
      



  