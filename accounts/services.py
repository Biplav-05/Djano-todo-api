from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from accounts.models import OTP, CustomUser
from accounts.serializers import LoginSerializer, OtpVerificationSerializer, ReSendOtpSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginService:
    def login(data):
        serializer = LoginSerializer(data=data)
        if(serializer.is_valid(raise_exception=True)):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate( email = email , password = password)

            if user is not None:
                usr = CustomUser.objects.get(email = email)
                if(usr.is_verified == True):

                    refresh = RefreshToken.for_user(user)
                    data = {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user_id': user.pk,
                        'Name' : user.firstname,
                        'email': user.email,
                        'message': 'Logged in'
                    }
                    return data
                    
                else:
                 return {'message' : 'User was not verified'}
            else : 
             return {'message' : 'Invalid username or password'}
        else :
         return {'message' : 'Invalid data entered'}



class OtpService:
    def verfy_otp(data):
        serializer = OtpVerificationSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']      
        try:
            user = get_object_or_404(CustomUser, email=email)
            otp_ = user.OTP 
            # print(f"otp_ object {otp_}")
            print(f"database otp  {otp_.otp}")

            if otp == otp_.otp:
                
                if not otp_.is_otp_verified():
                    
                    return {'message': 'OTP expired'}

                if user.is_verified:
                    return {'message': 'Provided OTP was already used'}
                
                user.is_verified = True
                user.save()

                return {'message': 'OTP verified'}
            else:
                return {'message': 'Invalid otp'}
            
        except CustomUser.DoesNotExist:
            return {'message': 'Invalid email'}
        
    def resend_otp(data):
        serializer = ReSendOtpSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = get_object_or_404(CustomUser, email=email)
            otp_ = OTP.objects.get(user = user)
            otp_.reset_otp()
            temp = otp_.generate_otp()
            print(f"Reseted otp of {user.firstname}  is {temp}")
            return {'message': 'Otp resent successfully'}
            
        except CustomUser.DoesNotExist:
            return {'message':'Email doesn`t exists'}


