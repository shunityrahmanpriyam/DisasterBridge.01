from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Donation

User = get_user_model()

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['name', 'email', 'phone_number', 'role', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(label="Email or Phone", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class LanguageForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['language_preference']
        widgets = {
            'language_preference': forms.Select(attrs={'class': 'form-control'})
        }