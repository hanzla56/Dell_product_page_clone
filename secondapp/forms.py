
from django.contrib.auth.forms import UserCreationForm
from .models import User_Data
from allauth.account.forms import SignupForm,LoginForm

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.pop('placeholder', None)

class LoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.pop('placeholder', None)
        
        
class SignUpForm(UserCreationForm):
    class Meta:
        model = User_Data
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email':'Email'}