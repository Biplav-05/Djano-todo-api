import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from todo_factory import TodoModelFactory
from rest_framework import status
from tests.accounts.factories import CustomUserFactory

@pytest.fixture
def client():
    return  APIClient()

@pytest.fixture
def authenticated_user():
    user = CustomUserFactory(email='test@email.com', password='test12345')
    return user

@pytest.fixture
def todo_data():
    data = TodoModelFactory.create()
    return data

@pytest.mark.django_db
def test_create_todo_view(authenticated_user,client,todo_data):
    client.force_authenticate(user=authenticated_user)
    url = reverse('todo-list')
    data = {
        'title':todo_data.title,
        'description':todo_data.description,
        'deadline':todo_data.deadline,
    }
    response = client.post(url, data=data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'id' in response.data
    assert 'title' in response.data
    assert 'description' in response.data
    assert 'deadline' in response.data

@pytest.mark.django_db
def test_list_todo_view(authenticated_user,client,todo_data):
    client.force_authenticate(user=authenticated_user)
    url = reverse('todo-list')
    response = client.get(url,format='json')
    assert response.status_code == status.HTTP_200_OK
    #assert  'a' in response.data

@pytest.mark.django_db
def test_detail_view(authenticated_user,client,todo_data):
    client.force_authenticate(user=authenticated_user)
    url = reverse('todo-details',args=[todo_data.id])
    response = client.get(url,format='json')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_update_todo_detail_view(authenticated_user,client,todo_data):
    client.force_authenticate(user=authenticated_user)
    url = reverse('todo-details',args=[todo_data.id])
    dummy_data = TodoModelFactory.create()
    data={
        'title':dummy_data.title,
        'description':dummy_data.description,
        'deadline':dummy_data.deadline,
        'isComplete':True,
    }
    response = client.put(url,data=data,format='json')
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_delete_todo_detail_view(authenticated_user,client,todo_data):
    client.force_authenticate(user=authenticated_user)
    url = reverse('todo-details',args=[todo_data.id])

    response = client.delete(url,format='json')
    assert response.status_code == status.HTTP_202_ACCEPTED