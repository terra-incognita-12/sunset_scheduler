import csv
from datetime import timedelta
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
	ScheduleDetailForm
)

from .models import (
	DefaultSchedule,
	Department,
	Employee,
	ScheduleProfile,
	CurrentSchedule,
	ScheduleDetail
)

from users.forms import (
	ChangeCompanyNameForm,
	ChangeUsernameForm,
	ChangeEmailForm,
)

@login_required(login_url='login_index')
def index(request):
	default_schedules = DefaultSchedule.objects.filter(user=request.user)
	departments = Department.objects.filter(user=request.user).annotate(employees_count=Count('employee'))
	employees = Employee.objects.filter(user=request.user)
	schedule_profiles = ScheduleProfile.objects.filter(user=request.user)
	current_schedule = CurrentSchedule.objects.filter(schedule_profile__user=request.user).first()
	if current_schedule:
		schedule_details = ScheduleDetail.objects.filter(schedule_profile=current_schedule.schedule_profile)
	else:
		schedule_details = []

	default_schedule_form = DefaultScheduleForm()
	department_form = DepartmentForm()
	employee_form = EmployeeForm()
	schedule_profile_form = ScheduleProfileForm()
	schedule_detail_form = ScheduleDetailForm()

	context = {
		'default_schedules': default_schedules,
		'departments': departments,
		'employees': employees,
		'schedule_profiles': schedule_profiles,
		'current_schedule': current_schedule,
		'schedule_details': schedule_details,

		'default_schedule_form': default_schedule_form,
		'department_form': department_form,
		'employee_form': employee_form,
		'schedule_profile_form': schedule_profile_form,
		'schedule_detail_form': schedule_detail_form,
	}

	return render(request, 'index/index.html', context)

@login_required(login_url='login_index')
def settings(request):

	change_company_name_form = ChangeCompanyNameForm()
	change_username_form = ChangeUsernameForm()
	change_email_form = ChangeEmailForm()

	context = {
		'change_company_name_form': change_company_name_form,
		'change_username_form': change_username_form,
		'change_email_form': change_email_form
	}

	return render(request, 'settings/settings.html', context)

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

### SCHEDULE DETAIL ###

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def schedule_detail_add(request):
	pk = request.POST['schedule_profile']
	schedule_profile = get_object_or_404(ScheduleProfile, pk=pk)
	form = ScheduleDetailForm(request.POST)
	if form.is_valid():
		schedule_detail_check_duplicate = ScheduleDetail.objects.filter(schedule_profile=schedule_profile, employee=form.cleaned_data.get('employee')).first()
		if schedule_detail_check_duplicate:
			messages.error(request, f"Employee \"{form.cleaned_data.get('employee')}\" already in schedule")
		else:
			schedule_detail = ScheduleDetail(schedule_profile=schedule_profile, **form.cleaned_data)
			schedule_detail.save()
	else:
		messages.error(request, form.errors)
	
	return redirect('index')

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def schedule_detail_update(request):
	schedule_profile_pk = request.POST['schedule_profile']
	pk = request.POST['hidden_id']
	schedule_detail = get_object_or_404(ScheduleDetail, pk=pk)
	schedule_profile = get_object_or_404(ScheduleProfile, pk=schedule_profile_pk)
	form = ScheduleDetailForm(request.POST, instance=schedule_detail)
	if form.is_valid():
		schedule_detail_check_duplicate = ScheduleDetail.objects.filter(schedule_profile=schedule_profile, employee=form.cleaned_data.get('employee')).first()
		if schedule_detail_check_duplicate and str(schedule_detail_check_duplicate.pk) != pk:
			messages.error(request, f"Employee \"{form.cleaned_data.get('employee')}\" already in schedule")
		else:
			schedule_detail.save()
	else:
		messages.error(request, form.errors)
			
	return redirect('index')

@login_required(login_url='login_index')
@require_http_methods(['POST'])
def schedule_detail_delete(request):
	for pk in request.POST.getlist('schedule_detail_delete'):
		schedule_detail = get_object_or_404(ScheduleDetail, pk=pk)
		schedule_detail.delete()
	
	return redirect('index')

### EXPORT ###

@login_required(login_url='login_index')
def export_schedule(request):
	schedule_fields = ['Name', 'Number', 'Mon', 'Tue', 'Wed', 'Thr', 'Fri', 'Sat', 'Sun']
	
	current_schedule = CurrentSchedule.objects.values_list('schedule_profile', 'schedule_profile__begin_date', 'schedule_profile__name').first()
	date_list = [current_schedule[1]+timedelta(days=i) for i in range(0, 7)]
	schedule = ScheduleDetail.objects.filter(schedule_profile=current_schedule[0]).values_list(
		'employee__name', 'employee__number',
		'mon_time', 'mon_duty', 'tue_time', 'tue_duty',
		'wed_time', 'wed_duty', 'thr_time', 'thr_duty',
		'fri_time', 'fri_duty', 'sat_time', 'sat_duty',
		'sun_time', 'sun_duty',
	)
	
	dates_row = []
	dates_row.append("")
	dates_row.append("")
	for elem in date_list:
		dates_row.append(elem.strftime("%m/%d/%Y"))
	# dates_row.append("")

	schedule_rows = []
	for line in list(schedule):
		row = []
		# name
		row.append(line[0])
		# number
		row.append(line[1])
		for i in range(2, len(line)-1, 2):
			time = line[i]
			duty = line[i+1]
			if not time:
				row.append('Off')
			elif not duty: 
				row.append(f'{time}')
			else:
				row.append(f'{line[i]}\n{line[i+1]}')
		schedule_rows.append(row)

	with open('foo.csv', 'w') as csv_file:
		csvwriter = csv.writer(csv_file)
		csvwriter.writerow(['Schedule ', current_schedule[2]])
		csvwriter.writerow(['Starts ', current_schedule[1].strftime("%m/%d/%Y")])
		csvwriter.writerow(schedule_fields)
		csvwriter.writerow(dates_row)
		csvwriter.writerows(schedule_rows)

	return redirect('index')