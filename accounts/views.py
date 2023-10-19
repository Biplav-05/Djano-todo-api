from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import *
from rest_framework import generics,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class CreateUser(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

class OtpVerificationView(generics.CreateAPIView):
    model = CustomUser
    serializer_class = OtpVerificationSerializer
    
    def post(self,request,*args,**kwargs):
        serializer = OtpVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']      
        try:
            user = get_object_or_404(CustomUser, email=email)
            otp_ = user.OTP 

            if otp == otp_.otp:
                
                if not otp_.is_otp_verified():
                    return Response({'message': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

                if user.is_verified:
                    return Response({'message': 'Provided OTP was already used'}, status=status.HTTP_400_BAD_REQUEST)
                
                user.is_verified = True
                user.save()

                return Response({'message': 'OTP verified', 'is_verified': True})
            else:
                return Response({'message': 'Invalid otp'}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({'message': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)


class ReSendOtpView(generics.CreateAPIView):

    serializer_class = ReSendOtpSerializer

    def post(self,request):
        serializer = ReSendOtpSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = get_object_or_404(CustomUser, email=email)
            OTP.reset_otp(user)
            OTP.generate_otp(user)
            print(f"Reseted otp of {user.firstname}  is {user.otp}")
            return Response({'message': 'Otp resent successfully'})
            
        except CustomUser.DoesNotExist:
            return Response({'message':'Email doesn`t exists'},status=status.HTTP_400_BAD_REQUEST)

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    
    def post(self,request):
        serializer = LoginSerializer(data=request.POST)
        if(serializer.is_valid(raise_exception=True)):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email = email , password = password)

            if user is not None:
                usr = CustomUser.objects.get(email = email)
                if(usr.is_verified == True):
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user_id': user.pk,
                        'Name' : user.firstname,
                        'email': user.email,
                        'message': 'Logged in'
                    })
                else:
                 return Response ({'message' : 'User was not verified'},status=status.HTTP_400_BAD_REQUEST)
            else : 
             return Response ({'message' : 'Invalid username or password'},status=status.HTTP_400_BAD_REQUEST)
        else :
         return Response ({'message' : 'Invalid data entered'},status=status.HTTP_400_BAD_REQUEST)
