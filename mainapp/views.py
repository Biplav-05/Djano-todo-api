from django.shortcuts import render
from rest_framework import generics,status
from .serializers import *
from .models import *
from rest_framework.permissions import *
from rest_framework.response import Response
from django.db.models import Count

#for login
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

# Views

class ListTodo(generics.ListAPIView):
    #permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = TodoModel.objects.order_by('-deadline').all();
    serializer_class = TodoSerializer


class TodoGroupedByDeadlineView(generics.ListAPIView):
    
    serializer_class = TodoGroupedByDeadlineSerializer

    def get_queryset(self):
        grouped_todos = TodoModel.objects.values('deadline').annotate(todo_count=Count('id')).order_by('deadline')
        return grouped_todos

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        response_data = []

        for group in queryset:
            todos_in_group = TodoModel.objects.filter(deadline=group['deadline'])
            serialized_todos = TodoSerializer(todos_in_group, many=True).data

            group_data = {
                'deadline': group['deadline'],
                'todo_count': group['todo_count'],
                'todos': serialized_todos,
            }

            response_data.append(group_data)

        return Response(response_data)


class DetailTodo(generics.RetrieveUpdateAPIView):
    queryset = TodoModel.objects.all();
    serializer_class = TodoSerializer


class CreateTodo(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = TodoModel.objects.all()
    serializer_class = TodoSerializer

class DeleteTodo(generics.RetrieveDestroyAPIView):
    queryset = TodoModel.objects.all()
    serializer_class = TodoSerializer 


class CreateUser(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED, headers=headers)

class OtpVerificationView(generics.CreateAPIView):
    model = CustomUser
    serializer_class = OtpVerificationSerializer
    

    def post(self,request,*args,**kwargs):
        serializer = OtpVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        try:
            user = CustomUser.objects.get(email = email , otp = otp)

        except CustomUser.DoesNotExist:
            return Response({'message': 'Invalid email or otp'},status=status.HTTP_400_BAD_REQUEST)
        
        if user.is_verified:
            return Response({'message': 'Provided otp wad already used '},status=status.HTTP_400_BAD_REQUEST)

        if user.is_otp_verified():
            user.is_verified = True
            user.save()
            return Response({'message':'OTP verified','is_verified':True})
        
        else:
            return Response({'message':'OTP expired'},status=status.HTTP_400_BAD_REQUEST)

class ReSendOtpView(generics.CreateAPIView):

    serializer_class = ReSendOtpSerializer

    def post(self,request):
        serializer = ReSendOtpSerializer(data=request.POST)
        if(serializer.is_valid()):
           email = serializer.validated_data['email']

           try:
            user = CustomUser.objects.get(email = email)
           except CustomUser.DoesNotExist:
            return Response({'message':'Email doesn`t exists'},status=status.HTTP_400_BAD_REQUEST)
        
           user.reset_otp()
           user.generate_otp()
           print(f"Reseted otp of {user.firstname}  is {user.otp}")
           return Response({'message': 'Otp resent successfully'})
        else:
           return Response({'message':'invalid data entered'},status=400)

class LoginView(generics.CreateAPIView):
    serializer_class = LoginSerializer
    
    def post(self,request):
        serializer = LoginSerializer(data=request.POST)
        if(serializer.is_valid()):
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email = email , password = password)

            if user is not None:
                usr = CustomUser.objects.get(email = email)
                if(usr.is_verified == True):
                 #return Response({'message' : 'Logged in '})
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user_id': user.pk,
                        'email': user.email,
                        'message': 'Logged in'
                    })
                else:
                 return Response ({'message' : 'User was not verified'},status=status.HTTP_400_BAD_REQUEST)
            else : 
             return Response ({'message' : 'Invalid username or password'},status=status.HTTP_400_BAD_REQUEST)
        else :
         return Response ({'message' : 'Invalid data entered'},status=status.HTTP_400_BAD_REQUEST)