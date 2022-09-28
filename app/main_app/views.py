from urllib import request
from django.shortcuts import render, redirect
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import (
	DefaultScheduleForm,
	DepartmentForm,
	EmployeeForm,
	ScheduleProfileForm,
)

from .models import (
	DefaultSchedule,
	Department,
	Employee,
	ScheduleProfile,
	CurrentSchedule,
)

@login_required(login_url='login_index')
def index(request):
	default_schedules = DefaultSchedule.objects.filter(user=request.user)
	departments = Department.objects.filter(user=request.user).annotate(employees_count=Count('employee'))
	employees = Employee.objects.filter(user=request.user)
	schedule_profiles = ScheduleProfile.objects.filter(user=request.user)
	current_schedule = CurrentSchedule.objects.filter(schedule_profile__user=request.user).first()

	default_schedule_form = DefaultScheduleForm()
	department_form = DepartmentForm()
	employee_form = EmployeeForm()
	schedule_profile_form = ScheduleProfileForm()

	context = {
		'default_schedules': default_schedules,
		'departments': departments,
		'employees': employees,
		'schedule_profiles': schedule_profiles,
		'current_schedule': current_schedule,

		'default_schedule_form': default_schedule_form,
		'department_form': department_form,
		'employee_form': employee_form,
		'schedule_profile_form': schedule_profile_form,
	}

	return render(request, 'index/index.html', context)

### DEFAULT SCHEDULE ###

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

### DEPARTMENT ###

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def department_add(request):
	form = DepartmentForm(request.POST)
	if form.is_valid():
		department = Department(user=request.user, **form.cleaned_data)
		department.save()
	else:
		messages.error(request, form.errors)
	
	return redirect('index')

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def department_update(request):
	pk = request.POST['hidden_id']
	department = get_object_or_404(Department, pk=pk)
	form = DepartmentForm(request.POST, instance=department)
	if form.is_valid():
		department.save()
	else:
		messages.error(request, form.errors)
	return redirect('index')

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def department_delete(request):
	for pk in request.POST.getlist('department_delete'):
		department = get_object_or_404(Department, pk=pk)
		department.delete()
	
	return redirect('index')

### EMPLOYEE ###

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def employee_add(request):
	form = EmployeeForm(request.POST)
	if form.is_valid():
		employee = Employee(user=request.user, **form.cleaned_data)
		employee.save()
	else:
		messages.error(request, form.errors)
	
	return redirect('index')

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def employee_update(request):
	pk = request.POST['hidden_id']
	employee = get_object_or_404(Employee, pk=pk)
	form = EmployeeForm(request.POST, instance=employee)
	if form.is_valid():
		employee.save()
	else:
		messages.error(request, form.errors)
	return redirect('index')

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def employee_delete(request):
	for pk in request.POST.getlist('employee_delete'):
		employee = get_object_or_404(Employee, pk=pk)
		employee.delete()
	
	return redirect('index')

### SCHEDULE PROFILE ###

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def schedule_profile_add(request):
	form = ScheduleProfileForm(request.POST)
	if form.is_valid():
		schedule_profile = ScheduleProfile(user=request.user, **form.cleaned_data)
		schedule_profile.save()
	else:
		messages.error(request, form.errors)
	
	return redirect('index')

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def schedule_profile_update(request):
	pk = request.POST['hidden_id']
	schedule_profile = get_object_or_404(ScheduleProfile, pk=pk)
	form = ScheduleProfileForm(request.POST, instance=schedule_profile)
	if form.is_valid():
		schedule_profile.save()
	else:
		messages.error(request, form.errors)
	return redirect('index')

@login_required(login_url='login_index')
@require_http_methods(['GET'])
def schedule_profile_delete(request, pk):
	schedule_profile = get_object_or_404(ScheduleProfile, pk=pk)
	schedule_profile.delete()

	return redirect('index')

### CURRENT SCHEDULE ###

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def current_schedule_pick(request):
	pk = request.POST['schedule_select']
	if not pk:
		messages.error(request, 'Pick up correct schedule')
		return redirect('index')

	current_schedule = CurrentSchedule.objects.filter(schedule_profile__user=request.user).first()
	if current_schedule:
		current_schedule.delete()

	schedule_profile = get_object_or_404(ScheduleProfile, pk=pk)
	current_schedule = CurrentSchedule(schedule_profile=schedule_profile)
	current_schedule.save()
	
	return redirect('index')