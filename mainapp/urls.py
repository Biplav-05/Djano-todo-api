from django.urls import path
from .views import *

urlpatterns =[
    path('',TodoListView.as_view(),name='todo-list'),
    path('<int:pk>/',TodoDetailView.as_view(),name='todo-details'),
]