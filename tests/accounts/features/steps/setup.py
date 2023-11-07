import os
from django import setup
os.environ['DJANGO_SETTINGS_MODULE'] = 'todo_list.settings'
setup()

from behave import given, when, then
from django.urls import reverse
from rest_framework.test import APIClient


@given('the api is running')
def step_given_api_running(context):
    context.client = APIClient()

@when('the user sends a POST request to \'/accounts/create-user/\' with the following data')
def step_when_user_sends_post_request(context):
    data = context.table[0].as_dict()
    response = context.client.post(reverse('create-user'), data, format="json")
    context.response = response
    print (context.response.content)

@then('the response status code should be 201')
def step_then_response_status_code_should_be(context):
    assert context.response.status_code == 201


