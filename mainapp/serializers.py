from rest_framework import serializers
from .models import *
from django.core.validators  import validate_email
from django.core.exceptions import ValidationError

# class TodoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TodoModel
#         fields =['id','title','description','deadline']

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoModel
        fields =['id','title','description','deadline','isComplete']

class TodoGroupedByDeadlineSerializer(serializers.Serializer):
    deadline = serializers.DateField()
    todo_count = serializers.IntegerField()
    todos = TodoSerializer(many=True)


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['firstname','lastname','email','password','confirm_password']
        extra_kwargs = {'password':{'write_only':True}}


    def validate(self,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("New and confirm password didn't match")
        
        try:
         validate_email(data['email'])
        except ValidationError:
            raise serializers.ValidationError("Invalid email format")

        return data

    def create(self,validate_data):
        validate_data.pop('confirm_password',None)
        user = CustomUser.objects.create_user(**validate_data)
        user.generate_otp()
        print(f"otp for user {user.firstname} : {user.otp}")
        return user;

class OtpVerificationSerializer(serializers.Serializer):
    email  = serializers.EmailField()
    otp = serializers.CharField(max_length = 16)

class ReSendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)