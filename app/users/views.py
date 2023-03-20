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
	ChangeCompanyNameForm,
	ChangeUsernameForm,
	ChangeEmailForm,
)

@unauthenticated_user
def login_index(request):
	login_form = LoginForm()
	register_form = RegisterForm()

	context = {
		'login_form': login_form,
		'register_form': register_form,
	}

	return render(request, 'users/login_index.html', context)	

### CHANGE ###

@login_required(login_url='login_index')
def change_company_name(request):
	User = get_user_model()

	form = ChangeCompanyNameForm(request.POST)
	if form.is_valid():
		email = request.POST['email']
		password = form.cleaned_data.get('password')
		company_name = form.cleaned_data.get('company_name')
		if not authenticate(email=email, password=password):
			messages.error(request, 'Wrong password')
		else:
			user = User.objects.get(email=email)
			user.company_name = company_name
			user.save()
			messages.success(request, 'Comapny changed successfully')
	else:
		errors = get_errors(form.errors)
		messages.error(request, errors)

	return redirect('settings')

@login_required(login_url='login_index')
def change_username(request):
	User = get_user_model()

	form = ChangeUsernameForm(request.POST)
	if form.is_valid():
		email = request.POST['email']
		password = form.cleaned_data.get('password')
		username = form.cleaned_data.get('username')
		if not authenticate(email=email, password=password):
			messages.error(request, 'Wrong password')
		else:
			user_check_duplicate = User.objects.filter(username=username).first()
			if user_check_duplicate:
				messages.error(request, f'Username {username} is already in use')
			else:
				user = User.objects.get(email=email)
				user.username = username
				user.save()
				messages.success(request, 'Username changed successfully')
	else:
		errors = get_errors(form.errors)
		messages.error(request, errors)

	return redirect('settings')

@login_required(login_url='login_index')
def change_email(request):
	User = get_user_model()

	form = ChangeEmailForm(request.POST)
	if form.is_valid():
		email = request.POST['old_email']
		new_email = form.cleaned_data.get('email')
		password = form.cleaned_data.get('password')
		if not authenticate(email=email, password=password):
			messages.error(request, 'Wrong password')
		else:
			user_check_duplicate = User.objects.filter(email=new_email).first()
			if user_check_duplicate:
				messages.error(request, f'Email {new_email} is already in use')
			else:
				user = User.objects.get(email=email)
				send_email_activation(request, user, new_email, is_change_email=True)
				messages.success(request, f'Activation link was sent to {new_email}')

	else:
		errors = get_errors(form.errors)
		messages.error(request, errors)

	return redirect('settings')

@login_required(login_url='login_index')
def change_email_done(request, uidb64, token, emailb64):
	User = get_user_model()
	
	try:
		uid = force_bytes(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except:
		user = None

	if user and account_activation_token.check_token(user, token):
		email = urlsafe_base64_decode(emailb64)
		user.email = email.decode()
		user.save()

		messages.success(request, 'Email changed successfully')
	else:
		messages.error(request, 'Activation link is invalid')

	return redirect('settings')

@login_required(login_url='login_index')
def password_change_done(request):
	messages.success(request, 'Password changed successfully')
	return redirect('settings')

### LOGIN ###

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
		errors = get_errors(form.errors)
		messages.error(request, errors)
	return redirect('login_index')

@login_required(login_url='login_index')
def logout(request):
	logout_django(request)
	return redirect('login_index')

### REGISTER ###

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
		errors = get_errors(form.errors)
		messages.error(request, errors)

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

######## SECONDARY ########

def send_email_activation(request, user, email, is_change_email=False):
	if is_change_email:
		mail_subject = 'Change your email'
		template_name = 'change_mail_activation'
	else:
		mail_subject = 'Activate your user account'
		template_name = 'mail_activation'

	message = render_to_string(f'users/activation/{template_name}.html', {
		'user': user.username,
		'domain': get_current_site(request).domain,
		'uid': urlsafe_base64_encode(force_bytes(user.pk)),
		'token': account_activation_token.make_token(user),
		'protocol': 'https' if request.is_secure() else 'http',
		'email': urlsafe_base64_encode(force_bytes(email))
	})
	email = EmailMessage(mail_subject, message, to=[email])
	if email.send():
		return True
	return False

def get_errors(form_errors):
	errors = ""

	for elem in form_errors.get_json_data(escape_html=False).items():
		for i in range(0, len(elem)):
			try:
				errors += f"<p>{elem[i][0]['message']}</p>"
			except TypeError: continue
	
	return errors