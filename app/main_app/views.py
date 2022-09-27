from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import (
	DefaultScheduleForm
)

from .models import (
	DefaultSchedule
)

@login_required(login_url='login_index')
def index(request):
	default_schedules = DefaultSchedule.objects.filter(user=request.user)

	default_schedule_form = DefaultScheduleForm()

	context = {
		'default_schedules': default_schedules,
		'default_schedule_form': default_schedule_form,
	}

	return render(request, 'index/index.html', context)

### default schedule ###

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def default_schedule_add(request):
	form = DefaultScheduleForm(request.POST)
	if form.is_valid():
		default_schedule = DefaultSchedule(user=request.user, **form.cleaned_data)
		default_schedule.save()
	else:
		messages.error(request, form.errors)
	
	return redirect('index')

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def default_schedule_update(request):
    pk = request.POST['hidden_id']
    default_schedule = get_object_or_404(DefaultSchedule, pk=pk)
    form = DefaultScheduleForm(request.POST, instance=default_schedule)
    if form.is_valid():
        default_schedule.save()
    else:
        messages.error(request, form.errors)
    return redirect('index') 

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def default_schedule_delete(request):
    for pk in request.POST.getlist('default_schedule_delete'):
        default_schedule = get_object_or_404(DefaultSchedule, pk=pk)
        default_schedule.delete()
    
    return redirect('index')