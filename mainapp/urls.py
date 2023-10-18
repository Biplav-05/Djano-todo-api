from django.urls import path
from .views import *

urlpatterns =[
    path('',TodoApiView.as_view(),name='todolist'),
    path('<int:pk>/',TodoApiView.as_view(),name='tododetails'),
    path('group-by',TodoGroupedView.as_view(),name='group-by-deadline'),
    path('list',TodoListView.as_view(),name='group-by-deadline'),
]