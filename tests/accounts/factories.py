import factory
from accounts.models import CustomUser,OTP
from django.contrib.auth.hashers import make_password 

class CustomUserFactory(factory.Factory):
    class Meta:
        model = CustomUser
        
    email = factory.Faker('email')
    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')
    is_verified = False
    
    username = factory.Faker('user_name')
    password = factory.LazyAttribute(lambda _: make_password('test12345'))
    
    @classmethod
    def create(cls, **kwargs):
        user = super().create(**kwargs)
        print(f"Created User: {user.email}")
        print(f"User Details: {user.email}, and password = {user.password}")
        return user
    
    
class OTPFactory(factory.Factory):
    class Meta:
        model = OTP
    
    user = factory.SubFactory(CustomUserFactory)
    otp = factory.Faker('random_int', min=100000, max=999999)