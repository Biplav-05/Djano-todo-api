from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from .models import *
from rest_framework.permissions import *
from rest_framework.response import Response
from django.http import Http404
from rest_framework import generics
from .services import *


class TodoListView(generics.ListAPIView):
    serializer_class = TodoSerializer
    
    def get_queryset(self):
        queryset = TodoListServices.list_todo(self.request)
        return queryset
    
    def list(self,request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)

class TodoGroupedView(generics.ListAPIView):
    serializer_class = TodoGroupedByDeadlineSerializer
    
    def get_queryset(self):
        queryset= TodoListServices.grouped_by_deadline();
        return queryset
    
    def list(self,request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset,many=True)
        return Response(serializer.data)
    
    
class TodoApiView(APIView):
    
    def get(self, request, pk=None):  
        if pk is not None:
            return self.get_detail(request, pk)
        else:
            return self.list_todos(request)
    
    def list_todos(self, request):
        result = TodoListServices.list_todo(request)
        return Response(result)        
    
    def post(self, request):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self, pk):
        try:
            return TodoModel.objects.get(pk=pk)
        except TodoModel.DoesNotExist:
            raise Http404(f"Todo with id {pk} doesnot exits ")

    def get_detail(self, request, pk):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    def put(self, request, pk):
        todo = self.get_object(pk)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        todo = self.get_object(pk)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
