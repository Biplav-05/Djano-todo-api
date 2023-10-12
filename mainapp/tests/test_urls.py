from django.test import SimpleTestCase
from django.urls import reverse,resolve
from mainapp.views import  *

class TestUrls(SimpleTestCase):
     
    def test_list_url_is_resolves(self):
        url = reverse('todolist')
        #print(resolve(url))
        self.assertEquals(resolve(url).func.view_class,ListTodo)

    def test_update_url_is_resolves(self):
        url = reverse('updatetodo',args=[1])
        self.assertEquals(resolve(url).func.view_class,DetailTodo)
    
    def test_delete_url_is_resolves(self):
        url = reverse('deletetodo',args=[2])
        self.assertEquals(resolve(url).func.view_class,DeleteTodo)

    def test_create_url_is_resolves(self):
        url = reverse('createtodo');
        self.assertEquals(resolve(url).func.view_class,CreateTodo)
    
    def test_create_user_url_is_resolves(self):
        url = reverse('createuser')
        self.assertEquals(resolve(url).func.view_class,CreateUser)

    def test_verify_otp_url_is_resolves(self):
        url = reverse('verify_otp')
        self.assertEquals(resolve(url).func.view_class,OtpVerificationView)

    def test_resend_otp_url_is_resloves(self):
        url = reverse('resend_otp')
        self.assertEquals(resolve(url).func.view_class,ReSendOtpView)

    def test_login_url_is_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func.view_class,LoginView)