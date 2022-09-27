from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.decorators import login_required

from .tokens import account_activation_token
from .decorators import unauthenticated_user

from .forms import (
	RegisterForm,
	LoginForm,
)

######## Main pages ########

@unauthenticated_user
def login_index(request):
	login_form = LoginForm()
	register_form = RegisterForm()

	context = {
		'login_form': login_form,
		'register_form': register_form,
	}

	return render(request, 'users/login_index.html', context)	

### login ###

@unauthenticated_user
def login(request):
	form = LoginForm(request.POST)
	if form.is_valid():
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(email=email, password=password)
		if not user.is_email_verified:
			return render(request, 'users/activation/not_activated.html', {'email': form.cleaned_data.get('email')})
		else:
			login_django(request, user)
			return redirect('index')
	else:
		messages.error(request, form.errors)
	return redirect('login_index')

@login_required(login_url='login_index')
def logout(request):
	logout_django(request)
	return redirect('login_index')

### register ###

@unauthenticated_user
def register(request):
	form = RegisterForm(request.POST)
	if form.is_valid():
		user = form.save()
		result = send_email_activation(request, user, form.cleaned_data.get('email'))
		if result:
			return redirect('activation')
		messages.error(request, 'Error occured while sending email, contact site administration please')
	else:
		messages.error(request, form.errors)

	return redirect('login_index')

@unauthenticated_user
def activation(request):
	return render(request, 'users/activation/activation.html', {})

def resend_activation(request):
	User = get_user_model()

	email = request.POST['email']
	user = User.objects.get(email=email)
	send_email_activation(request, user, email)
	return redirect('activation')

@unauthenticated_user
def activation_done(request, uidb64, token):
	User = get_user_model()
	try:
		uid = force_bytes(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except:
		user = None

	if user and account_activation_token.check_token(user, token):
		user.is_email_verified = True
		user.save()

		messages.success(request, 'Now you can login in your account')
	else:
		messages.error(request, 'Activation link is invalid')

	return redirect('login_index')

######## Secondary ########

def send_email_activation(request, user, email):
	mail_subject = 'Activate your user account'
	message = render_to_string('users/activation/mail_activation.html', {
		'user': user.username,
		'domain': get_current_site(request).domain,
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': account_activation_token.make_token(user),
		'protocol': 'https' if request.is_secure() else 'http'
	})
	email = EmailMessage(mail_subject, message, to=[email])
	if email.send():
		return True
	return False