from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.permissions import *
from rest_framework.response import Response
from .services import *
from rest_framework import status

class TodoListView(APIView):
    def get(self,request):
        if 'deadline' in request.query_params:
            result = TodoListServices.list_todo(request)
        elif 'group' in request.query_params:
            result = TodoListServices.grouped_by_deadline(request)
        else:
            result = {'message':'invalid query parameter'}
        return Response(result)
    
    def post(self,request):
        result =  TodoListServices.create_todo(request.data)
        return Response(result)
    
    
class TodoDetailView(APIView):
    def get(self,pk):
        result = TodoListServices.get_todo_detail(pk)
        return Response(result,status = status.HTTP_200_OK)
       
    def put(self,request,pk):
        result = TodoListServices.update_todo(pk,request.data)
        return Response(result,status=status.HTTP_200_OK)
    
    def delete(self,pk):
        result = TodoListServices.delete_todo(pk)
        return Response(result,status=status.HTTP_202_ACCEPTED)