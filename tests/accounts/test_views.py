import pytest
from django.urls import reverse
from .factories import CustomUserFactory,OTPFactory

@pytest.fixture
def authenticated_client(client):
    user = CustomUserFactory.create(email ='test@gmail.com',password='test12345')
    client.force_authenticate(user=user)
    return client

@pytest.mark.django_db
def test_create_user_view(authenticated_client):
    url = reverse('create-user')
    user_data = {
        'email':'test@example.com',
        'firstname':'Test',
        'lastname':'Data',
        'password':'testpassword',
        'confirm_password':'testpassword',
    }
    
    response = authenticated_client.post(url,data=user_data,format='json')
    assert response.status_code == 201
   

@pytest.mark.django_db
def test_login_view(authenticated_client):
    url = reverse('login')
    user_data = {
        'email': 'test@gmail.com',
        'password':'test12345',
    }
    response = authenticated_client.post(url,data=user_data,format='json')
    assert 'message' in response.data
    
    
    
@pytest.mark.django_db
def test_otp_verification_view(authenticated_client):
    url = reverse('verify-otp')
    user = CustomUserFactory.create()
    otp = OTPFactory.create(user=user)
    otp_data = {
        'email': user.email,
        'otp': otp.otp,
    }

    response = authenticated_client.post(url, data=otp_data, format='json')
    assert response.status_code == 404
   
    
