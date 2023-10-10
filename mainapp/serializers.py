from rest_framework import serializers
from .models import *

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoModel
        fields =['id','title','description','date','isComplete']

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username','email','password']
        extra_kwargs = {'password':{'write_only':True}}

    def create(self,validate_data):
        user = CustomUser.objects.create_user(**validate_data)
        user.generate_otp()
        print(f"otp for user {user.username} : {user.otp}")
        return user;