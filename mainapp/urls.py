from django.urls import path
from .views import *

#import packages related to jwt authentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns =[
    path('',ListTodo.as_view(),name='todolist'),
    path('<int:pk>/',DetailTodo.as_view(),name='updatetodo'),
    path('create/',CreateTodo.as_view(),name='createtodo'),
    path('delete/<int:pk>',DeleteTodo.as_view(),name='deletetodo'),

    #for jwt auth
    #path('token/',TokenObtainPairView.as_view(),name='tokenview'),
    #path('refresh_token',TokenRefreshView.as_view(),name='refreshtoken'),

    #for User 
    path('createuser/',CreateUser.as_view(),name='createuser'),
    path("verify_otp/", OtpVerificationView.as_view(), name="verify_otp"),
    path('resend_otp/',ReSendOtpView.as_view(),name='resend_otp'),
    path('login/',LoginView.as_view(),name='login')
    
]