from django.test import TestCase
from mainapp.models import *
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from mainapp.serializers import *
from mainapp.models import CustomUser
from datetime import timedelta


User = get_user_model()

class TestView(TestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.create_user_url = '/createuser/'
        self.otp_verification_url = '/verify_otp/'
        self.otp_resend_url = '/resend_otp/'
        
        
    
    #create user with valid data
    def test_create_valid_user(self):
        data = {
            'firstname' :'Nanu',
            'lastname' : 'Tamang',
            'email' : 'mansi@gmail.com',
            'password' : 'nanu@123',
            'confirm_password' : 'nanu@123'
        }
    
        #serialize the data and check serializer is valid or not
        serializer = UserRegistrationSerializer(data = data)
        self.assertTrue(serializer.is_valid())

        #make a post request to the view
        response = self.client.post(self.create_user_url,data,format='json')

        #Check the status code is 201_created or not
        self.assertEquals(response.status_code,status.HTTP_201_CREATED);
    
    #try to create a user with invalid data
    def test_create_invalid_user(self):

        User.objects.create(firstname = 'Dummy',lastname = 'Data', email = 'bibash@gmail.com', password = 'test@123')

        data = {
            'firstname' :'Dummy',
            'lastname' : 'Data',
            'email' : 'bibash@gmail.com',
            'password' : 'test@123',
            'confirm_password' : 'test@123'
        }
        #make a post request to the view
        response = self.client.post(self.create_user_url,data,format="json")

        #Check the status code is 404_Bad_Request or not
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn('email',response.data)
        self.assertEquals(response.data['email'][0].code,'unique')


    #Otp Verification
    def test_OtpVerificationView(self):
        usr = CustomUser.objects.create(firstname = 'Dummy',lastname = 'Data', email = 'bibash@gmail.com', password = 'test@123')
        usr.otp = '123456'

        #usr.otp_created_at = datetime.now()
        
        usr.otp_created_at = datetime.now()-timedelta(minutes = 5);
        usr.save()

        data = {
            'email' : 'bibash@gmail.com',
            'otp': '123456'
        }
        response = self.client.post(self.otp_verification_url,data,format='json')
        #self.assertEquals(response.status_code,status.HTTP_200_OK)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ReSendOtpView(self):
        usr = CustomUser.objects.create(firstname = 'Dummy',lastname = 'Data', email = 'bibash@gmail.com', password = 'test@123')
        usr.save()
        usr.otp_created_at = datetime.now()-timedelta(minutes = 5);
        usr.save()
        data = {
            'email':'bibash@gmail.com'
        }
        response = self.client.post(self.otp_resend_url,data,format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        print(response.data)