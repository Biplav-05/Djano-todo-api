from django.urls import path
from .views import *

#for User 
urlpatterns = [
    path('createuser/',CreateUser.as_view(),name='create-user'),
    path("verify_otp/", OtpVerificationView.as_view(), name="verify-otp"),
    path('resend_otp/',ResendOtpView.as_view(),name='resend-otp'),
    path('login/',LoginView.as_view(),name='login')
]
    