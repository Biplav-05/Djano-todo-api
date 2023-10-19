from .models import TodoModel
from .serializers import TodoSerializer
from django.db.models import Count
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404


class TodoListServices:  
    def list_todo(request):
        queryset = TodoModel.objects.order_by('-deadline').all()
        paginator = PageNumberPagination()
        paginator.page_size = 5
        page = paginator.paginate_queryset(queryset,request)
            
        serializer = TodoSerializer(page,many=True) if page else TodoSerializer(queryset,many=True)
        return serializer.data
        
    def grouped_by_deadline(request):
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

        return response_data
    
    def create_todo(data):
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return serializer.errors
    
    def update_todo(pk,data):
        todo = get_object_or_404(TodoModel,pk=pk)
        serializer = TodoSerializer(todo, data=data)
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        return serializer.errors
    
    def delete_todo(pk):
        todo =get_object_or_404(TodoModel,pk=pk)
        todo.delete()
        return {'message':'deleted successfully'}
    
    def get_todo_detail(pk):
        todo = get_object_or_404(TodoModel,pk=pk)
        serializer = TodoSerializer(todo)
        return serializer.data
        