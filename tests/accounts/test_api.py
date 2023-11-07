import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import CustomUserFactory, OTPFactory
from rest_framework import status
from django.contrib.auth.hashers import make_password

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def test_otp_user():
    user = CustomUserFactory(email='test@email.com', password='test12345')
    otp = OTPFactory(user=user)
    return user, otp

@pytest.mark.django_db
def test_create_user_view(client):
    url = reverse('create-user')
    user_data = {
        'email': 'test@example.com',
        'firstname': 'Test',
        'lastname': 'Data',
        'password': 'testpassword',
        'confirm_password': 'testpassword',
    }
    response = client.post(url, data=user_data, format='json')
    assert response.status_code == 201
    
@pytest.mark.django_db()
def test_login_view(client):
    user = CustomUserFactory.create(email='test@email.com', password=make_password('test12345'),is_verified=True)
    url = reverse('login')
    user_data = {
        'email': user.email,
        'password': 'test12345',
    }
    response = client.post(url, data=user_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert 'refresh' in response.data
    assert 'user_id' in response.data
    assert 'Name' in response.data
    assert 'email' in response.data
    assert 'message' in response.data
    assert response.data['message'] == 'Logged in'
    
@pytest.mark.django_db
def test_otp_verification_view(client, test_otp_user):
    url = reverse('verify-otp')
    user,otp = test_otp_user
    otp_data = {
        'email': user.email,
        'otp': otp.otp,
    }
    response = client.post(url, data=otp_data, format='json')
    assert response.status_code == 200
    assert 'message' in response.data
    assert response.data['message'] == 'OTP verified'
    
@pytest.mark.django_db
def test_otp_resendotp_view(client,test_otp_user):
    url = reverse('resend-otp')
    user, _ = test_otp_user
    data = {
        'email' : user.email
    }
    response = client.put(url,data=data,format='json')
    assert response.status_code == 200
    assert 'message' in response.data
    assert response.data['message'] == 'Otp resent successfully'
    
