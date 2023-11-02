import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from .factories import CustomUserFactory, OTPFactory
from rest_framework import status

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def test_user():
    return CustomUserFactory.create(email='test@gmail.com', password='test12345',is_verified=True)

@pytest.fixture
def test_otp(test_user):
    return OTPFactory.create(user=test_user)

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
    

@pytest.mark.django_db(transaction=False)
def test_login_view(client, test_user):
    user = CustomUserFactory(password='test12345',is_verified=True)
    url = reverse('login')
    user_data = {
        'email': user.email,
        'password': 'test12345',
    }

    response = client.post(url, data=user_data, format='json')

    assert response.status_code == status.HTTP_200_OK
    print(response.data)
    assert 'refresh' in response.data
    
    if 'access' in response.data:
        # Successful login
        assert 'refresh' in response.data
        assert 'user_id' in response.data
        assert 'Name' in response.data
        assert 'email' in response.data
        assert 'message' in response.data
        assert response.data['message'] == 'Logged in'
    else:
        # Invalid login
        assert 'message' in response.data
        assert response.data['message'] == 'Invalid username or password'
    
@pytest.mark.django_db
def test_otp_verification_view(client, test_otp):
    url = reverse('verify-otp')
    otp_data = {
        'email': test_otp.user.email,
        'otp': test_otp.otp,
    }

    response = client.post(url, data=otp_data, format='json')
    assert response.status_code == 404
