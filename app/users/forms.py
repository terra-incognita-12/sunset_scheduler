import re

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate

from .models import CustomUser

class LoginForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = CustomUser
		fields = ['email', 'password']
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'form-control'}),
		}

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data.get('email')
			password = self.cleaned_data.get('password')
			if not authenticate(email=email, password=password):
				raise forms.ValidationError('Invalid Login and/or password')


class RegisterForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ['username', 'email', 'password1', 'password2', 'company_name']
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control', 'id': 'register_userername'}),
			'email': forms.EmailInput(attrs={'class': 'form-control'}),
			'company_name': forms.TextInput(attrs={'class': 'form-control', 'id': 'register_company'})
		}

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].help_text = mark_safe("<ul><li>Username should be longer than 8 and less than 30 symbols</li><li>Username allowed letters, digits, also dot and underscore (can't duplicate, go one after another, be last or first symbol)</li></ul>")
		self.fields['email'].required = True
		self.fields['company_name'].label = 'Comapny name'
		self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'id': 'register_pass1'})
		self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'id': 'register_pass2', 'onkeyup': 'password_matching();'})

	def clean_email(self):
		email = self.cleaned_data.get('email').lower()
		try:
			user = CustomUser.objects.get(email=email)
		except Exception as e:
			return email
		raise forms.ValidationError(f'Email {email} is already in use')

	def clean_username(self):
		username = self.cleaned_data.get('username')

		if len(username) < 8 or len(username) > 30:
			raise forms.ValidationError('Username should be longer than 8 and less than 30 symbols')

		patt = re.search("^(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$", username)
		if not patt:
			raise forms.ValidationError("Username allowed letters, digits, also dot and underscore (can't duplicate, go one after another, be last or first symbol)")

		try:
			user = CustomUser.objects.get(username=username)
		except Exception as e:
			return username
		
		raise forms.ValidationError(f'Username {username} is already in use')

class ChangeCompanyNameForm(forms.ModelForm):
	password = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = CustomUser
		fields = ['company_name', 'password']
		widgets = {
			'company_name': forms.TextInput(attrs={'class': 'form-control'})
		}

	def __init__(self, *args, **kwargs):
		super(ChangeCompanyNameForm, self).__init__(*args, **kwargs)
		self.fields['company_name'].label = 'New company name'

class ChangeUsernameForm(forms.ModelForm):
	password = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = CustomUser
		fields = ['username', 'password']
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control'})
		}

	def __init__(self, *args, **kwargs):
		super(ChangeUsernameForm, self).__init__(*args, **kwargs)
		self.fields['username'].label = 'New username'

	def clean_username(self):
		username = self.cleaned_data.get('username')

		if len(username) < 8 or len(username) > 30:
			raise forms.ValidationError('Username should be longer than 8 and less than 30 symbols')

		patt = re.search("^(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$", username)
		if not patt:
			raise forms.ValidationError("Username allowed letters, digits, also dot and underscore (can't duplicate, go one after another, be last or first symbol)")

		return username

class ChangeEmailForm(forms.ModelForm):
	password = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	class Meta:
		model = CustomUser
		fields = ['email', 'password']
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		super(ChangeEmailForm, self).__init__(*args, **kwargs)
		self.fields['email'].label = 'New email'