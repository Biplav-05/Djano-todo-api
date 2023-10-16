from django.test import TestCase
from mainapp.models import *
from django.contrib.auth.models import User



class ModelTest(TestCase):

    def test_create_user(self):
        email = "test@example.com"
        firstname = "test"
        lastname = "test"
        password = "testpass"

        user = CustomUser.objects.create_user(email = email , firstname = firstname, lastname = lastname, password = password)
        
        self.assertEqual(user.email, email)
        self.assertEqual(user.firstname,firstname)
        self.assertEqual(user.lastname,lastname)
        self.assertTrue(user.check_password(password))

    def test_super_user(self):
        email = "superusers@example.com"
        firstname = "Super"
        lastname = "User"
        password = "admin@123"

        superuser = CustomUser.objects.create_superuser(email = email , firstname = firstname, lastname = lastname, password = password)
        
        self.assertEqual(superuser.email, email)
        self.assertEqual(superuser.firstname,firstname)
        self.assertEqual(superuser.lastname,lastname)
        self.assertTrue(superuser.check_password(password))   
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)

class test_todo_model(TestCase):
    
    def setUp(self):
        self.todo = TodoModel.objects.create(
            title = 'Test Task',
            description = 'Test description',
            deadline = (2023,10,5),
            isComplete = False
            )
        self.todo.save()

    #def test_todo_model_fields(self):

        # save_todo = TodoModel.objects.get(id=self.todo.id)
        # print(save_todo)
        
        # #Test the fields
        # self.assertTrue(save_todo.title,'Test Task')
        

       
