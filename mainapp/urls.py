from django.urls import path
from .views import *

#import packages related to jwt authentication
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns =[
    path('',ListTodo.as_view()),
    path('<int:pk>/',DetailTodo.as_view()),
    path('create/',CreateTodo.as_view()),
    path('delete/<int:pk>',DeleteTodo.as_view()),

    #for jwt auth
    path('token/',TokenObtainPairView.as_view(),name='tokenview'),
    path('refresh_token',TokenRefreshView.as_view(),name='refreshtoken'),

    #for User 
    path('createuser/',CreateUser.as_view(),name='createuser')
]