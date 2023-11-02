import factory
from accounts.models import CustomUser,OTP


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        
    email = factory.Faker('email')
    firstname = factory.Faker('first_name')
    lastname = factory.Faker('last_name')
    is_verified = False
    
    username = factory.Faker('user_name')
    
    @classmethod
    def create(cls, **kwargs):
        user = super().create(**kwargs)
        print(f"Created User: {user.email}")
        print(f"User Details: {user.email}, and password = {user.password}")
        return user
    
    
class OTPFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OTP
    
    user = factory.SubFactory(CustomUserFactory)
    otp = factory.Faker('random_int', min=100000, max=999999)