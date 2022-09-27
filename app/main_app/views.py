from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='login_index')
def index(request):
	return render(request, 'index/index.html', {})