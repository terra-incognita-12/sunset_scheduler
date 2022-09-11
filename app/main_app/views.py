from django.shortcuts import render
from django.contrib import auth

from .forms import RegisterForm

def index(request):
	return render(request, 'index/index.html', {})

def login(request):
	register_form = RegisterForm()

	context = {
		'register_form': register_form,
	}

	return render(request, 'auth/login.html', context)