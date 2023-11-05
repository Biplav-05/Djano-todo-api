from rest_framework.views import APIView
from .serializers import *
from .models import *
from rest_framework.permissions import *
from rest_framework.response import Response
from .services import *
from rest_framework import status

class TodoListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        if 'group' in request.query_params:
            result = TodoListServices.grouped_by_deadline(request)
            
        else:
            result = TodoListServices.list_todo(request)
        return Response(result)
    
    def post(self,request):
        result =  TodoListServices.create_todo(request.data)
        return Response(result)
    
    
class TodoDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        result = TodoListServices.get_todo_detail(pk)
        return Response(result,status = status.HTTP_200_OK)
       
    def put(self,request,pk):
        result = TodoListServices.update_todo(pk,request.data)
        return Response(result,status=status.HTTP_200_OK)
    
    def delete(self,request,pk):
        result = TodoListServices.delete_todo(pk)
        return Response(result,status=status.HTTP_202_ACCEPTED)