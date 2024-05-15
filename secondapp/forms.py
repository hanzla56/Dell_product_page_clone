from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import User_Data

class SignUpForm(UserCreationForm):
    class Meta:
        model = User_Data
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email':'Email'}