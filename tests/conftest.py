import pytest
from rest_framework.test import APIClient

@pytest.fixture
def client():
    return APIClient()
    
@pytest.fixture
def payload():
    data = [
        #Create user
        {'email':'test@gmail.com','firstname':'Test','lastname':'data','password':'testpass','confirm_password':'testpass'},
        #create user with  incorrect password
         {'email': 'test3@gmail.com','firstname': 'Test3','lastname': 'data3','password': 'testpass3','confirm_password': 'testpc'},
         #create user with  invalid email
         {'email': 'test3@gmail.','firstname': 'Test3','lastname': 'data3','password': 'testpass3','confirm_password': 'testpc'},
    ]
    return data
