from django.urls import resolve,reverse
from accounts.views import CreateUser,LoginView,OtpVerificationView,ResendOtpView

def test_create_user_url():
    url = reverse('create-user')
    assert resolve(url).func.view_class == CreateUser
    
def test_login_view_url():
    url = reverse('login')
    assert resolve(url).func.view_class == LoginView
    
def test_otp_verification_view_url():
    url = reverse('verify-otp')
    assert resolve(url).func.view_class == OtpVerificationView
    
def test_resend_otp_view_url():
    url = reverse('resend-otp')
    assert resolve(url).func.view_class == ResendOtpView