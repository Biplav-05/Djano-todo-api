import pytest
from rest_framework import status
from unittest.mock import patch
from accounts.services import LoginService,OtpService
from .mock_services import MockedLoginService,MockOtpService
from django.test import RequestFactory
from django.urls import reverse
from accounts.views import LoginView,OtpVerificationView


@pytest.fixture
def factory():
    return RequestFactory()

#Login view test
@pytest.mark.django_db
def test_login_view_with_valid_credentials(factory):
    request_data = {'email':'valid@gmail.com', 'password':'password'}
    request = factory.post(reverse('login'),data=request_data)
    with patch.object(LoginService, 'login', return_value=MockedLoginService.login(request_data)):
        response = LoginView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == 'Logged in'

@pytest.mark.django_db
def test_login_view_with_unverified_credentials(factory):
    request_data = {'email':'unverified@gmail.com', 'password':'password'}
    request = factory.post(reverse('login'),data=request_data)
    with patch.object(LoginService, 'login', return_value=MockedLoginService.login(request_data)):
        response = LoginView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == 'User was not verified'

@pytest.mark.djnago_db
def test_login_view_with_invalid_credentails(factory):
    request_data = {'email':'invalid@mail.com','password':'invalidpassword'}
    request = factory.post(reverse('login'),data=request_data)
    with patch.object(LoginService,'login',return_value=MockedLoginService.login(request_data)):
        response = LoginView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == 'Invalid username or password'

#otp verification view
@pytest.mark.dajngo_db
def test_otpverification_view_with_valid_data(factory):
    request_data = {'email':'verify@gmail.com','otp':'123456'}
    request = factory.post(reverse('verify-otp'),data=request_data)
    with patch.object(OtpService,'verify_otp',return_value=MockOtpService.verify_otp(request_data)):
        response = OtpVerificationView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == 'OTP verified'

@pytest.mark.django_db
def test_otpverification_view_with_already_used_otp(factory):
    request_data = {'email':'already@example.com','otp':'456789'}
    request = factory.post(reverse('verify-otp'),data=request_data)
    with patch.object(OtpService,'verify_otp',return_value=MockOtpService.verify_otp(request_data)):
        response = OtpVerificationView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        assert response.data['message'] == 'Provided OTP was already used'

@pytest.mark.django_db
def test_otpverification_view_with_expired_otp(factory):
    request_data = {'email':'expired@example.com','otp':'112233'}
    request = factory.post(reverse('verify-otp'),data=request_data)
    with patch.object(OtpService,'verify_otp',return_value=MockOtpService.verify_otp(request_data)):
        response = OtpVerificationView.as_view()(request)
        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data 
        assert response.data['message'] == 'OTP expired'


# @pytest.mark.django_db
# def test_otpverification_view_with_invalid_user_email(factory):


