from rest_framework import serializers
from .models import *

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoModel
        fields =['id','title','description','deadline','isComplete']

class TodoGroupedByDeadlineSerializer(serializers.Serializer):
    deadline = serializers.DateField()
    todo_count = serializers.IntegerField()
    todos = TodoSerializer(many=True)

