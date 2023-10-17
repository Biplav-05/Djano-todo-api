from django.urls import path
from .views import *

#for User 
urlpatterns = [
    path('createuser/',CreateUser.as_view(),name='createuser'),
    path("verify_otp/", OtpVerificationView.as_view(), name="verify_otp"),
    path('resend_otp/',ReSendOtpView.as_view(),name='resend_otp'),
    path('login/',LoginView.as_view(),name='login')
]
    