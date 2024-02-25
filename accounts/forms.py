from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ['email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']


class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ['email', 'first_name', 'last_name', 'phone_number']

class CustomLoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())






