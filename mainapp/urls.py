from django.urls import path
from .views import *

urlpatterns =[
    path('todos/',TodoApiView.as_view(),name='todolist'),
    path('todos/<int:pk>',TodoApiView.as_view(),name='tododetails'),
    path('todos/group-by',TodoApiView.as_view(),name='group-by-deadline'),
]