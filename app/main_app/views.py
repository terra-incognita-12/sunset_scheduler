from django.shortcuts import render

def index(request):
	return render(request, 'index/index.html', {})

def login(request):
	return render(request, 'auth/login.html', {})