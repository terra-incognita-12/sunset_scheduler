from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):

	company_name = forms.CharField(
		label='Company Name',
		max_length=255, 
		widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'register_company'}),
	)

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2', 'company_name']
		widgets = {
			'username': forms.TextInput(attrs={
				'class': 'form-control', 
				'id': 'register_user',
			}),
			'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'register_email'
            }),
		}

	def __init__(self, *args, **kwargs):
		super(RegisterForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True
		self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'id': 'register_pass1'})
		self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'id': 'register_pass2'})