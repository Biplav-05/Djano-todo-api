from django.urls import resolve,reverse
from mainapp.views import TodoListView,TodoDetailView

def test_todoListView():
    url = reverse('todo-list')
    assert resolve(url).func.view_class == TodoListView

def test_todoDetailView():
    url = reverse('todo-details',args=[1])
    assert resolve(url).func.view_class == TodoDetailView


