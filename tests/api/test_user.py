import pytest
import json

@pytest.mark.django_db
def test_create_user(client,payload):
    response = client.post("/createuser/",data = payload[0], format="json")
    assert response.status_code == 201
    data = json.loads(response.content)
    assert data["message"] == "User registered successfully";
   
@pytest.mark.django_db
def test_failed_create_user_password_error(client,payload):
    response = client.post("/createuser/",data = payload[1], format="json")
    assert response.status_code == 400
    
    data = json.loads(response.content)
    assert "non_field_errors" in data
    assert "New and confirm password didn't match" in data["non_field_errors"]
    
@pytest.mark.django_db
def test_failed_create_user_invalid_email(client,payload):
    response = client.post("/createuser/",data=payload[2],format="json")
    assert response.status_code == 400
    
    data = json.loads(response.content)
    assert 'email' in data
    assert "Enter a valid email address." in data['email']

    
