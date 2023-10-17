from rest_framework.views import APIView
from django.shortcuts import render
from rest_framework import generics,status
from .serializers import *
from .models import *
from rest_framework.permissions import *
from rest_framework.response import Response
from django.db.models import Count
from django.http import Http404
from rest_framework.pagination import PageNumberPagination

class TodoApiView(APIView):
    
    def get(self, request, pk=None):  
        if pk is not None:
            return self.get_detail(request, pk)
        elif 'group-by' in request.path:
            return self.grouped_by_deadline(request)
        else:
            return self.list_todos(request)
    
    def list_todos(self, request):
        queryset = TodoModel.objects.order_by('-deadline').all()
        paginator = PageNumberPagination()
        paginator.page_size = 5
        page = paginator.paginate_queryset(queryset,request)
            
        serializer = TodoSerializer(page,many=True) if page else TodoSerializer(queryset,many=True)
        result = {
                'count': paginator.page.paginator.count,
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'result':serializer.data,
            } 
        return Response(result)
    
    def grouped_by_deadline(self,request):
        grouped_todos = TodoModel.objects.values('deadline').annotate(todo_count=Count('id')).order_by('deadline')
        response_data = []
        for group in grouped_todos:
            todos_in_group = TodoModel.objects.filter(deadline=group['deadline'])
            serialized_todos = TodoSerializer(todos_in_group, many=True).data

            group_data = {
                'deadline': group['deadline'],
                'todo_count': group['todo_count'],
                'todos': serialized_todos,
            }

            response_data.append(group_data)

        return Response(response_data)
        
    
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
    
