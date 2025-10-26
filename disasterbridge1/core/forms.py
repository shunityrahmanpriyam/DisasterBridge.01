
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Donation
from .models import AidRequest
from .models import LiveUpdate


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

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            'donation_type',
            'amount',
            'items_title',
            'items_description',
            'payment_method',
            'receipt_number',
            'pickup_date',
            'pickup_time',
            'pickup_address',
        ]
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'}),
            'items_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item title'}),
            'items_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'pickup_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'receipt_number': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }


class AidRequestForm(forms.ModelForm):
    class Meta:
        model = AidRequest
        fields = ["location", "latitude", "longitude", "category", "urgency", "voice_message", "photo", "notes"]
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

class LiveUpdateForm(forms.ModelForm):
    class Meta:
        model = LiveUpdate
        fields = ["category", "title", "description", "volunteer_name", "location", "image"]

