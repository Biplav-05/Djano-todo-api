from django.shortcuts import render
from rest_framework import generics,status
from .serializers import *
from .models import *
from rest_framework.permissions import *
from rest_framework.response import Response


# Create your views here.

class ListTodo(generics.ListAPIView):
    #permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = TodoModel.objects.all();
    serializer_class = TodoSerializer

class DetailTodo(generics.RetrieveUpdateAPIView):
    queryset = TodoModel.objects.all();
    serializer_class = TodoSerializer


class CreateTodo(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = TodoModel.objects.all()
    serializer_class = TodoSerializer

class DeleteTodo(generics.RetrieveDestroyAPIView):
    queryset = TodoModel.objects.all()
    serializer_class = TodoSerializer 


class CreateUser(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED, headers=headers)


    