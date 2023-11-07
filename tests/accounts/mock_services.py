from unittest.mock import Mock

class MockedLoginService(Mock):
    def login(data):
        print(data)
        if data.get('email') == 'valid@gmail.com' and data.get('password') == 'password':
            return {'message':'Logged in'}
        elif data.get('email') == 'unverified@gmail.com' and data.get('password') == 'password':
            return {'message':'User was not verified'}
        else:
            return {'message':'Invalid username or password'}

class MockOtpService(Mock):
    def verify_otp(data):
        if data.get('email') == 'verify@gmail.com' and data.get('otp') == '123456':
            return {'message':'OTP verified'}
        elif data.get('email') == 'already@example.com' and data.get('otp') == '456789':
            return {'message':'Provided OTP was already used'}
        elif data.get('email') == 'expired@example.com' and data.get('otp') == '112233':
            return {'message':'OTP expired'}
        elif data.get('email') == 'nonuser@mail.com' and data.get('otp') == '112233':
            return {'message':'Invalid email'}
        else:
            return {'message':'Invalid otp'}