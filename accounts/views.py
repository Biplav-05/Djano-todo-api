from accounts.services import LoginService, OtpService
from .serializers import *
from .models import *
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

class CreateUser(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    
    def post(self,request):
        result = LoginService.login(request.data)
        return Response(result)
        
class OtpVerificationView(generics.CreateAPIView):
    serializer_class = OtpVerificationSerializer
    
    def post(self,request):
        result = OtpService.verfy_otp(request.data)
        return Response(result)

class ResendOtpView(APIView):
    serializer_class = ReSendOtpSerializer
    
    def put(self,request):
        result = OtpService.resend_otp(request.data)
        return Response(result)
        

