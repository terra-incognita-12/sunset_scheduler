import re
from django import forms

from .models import (
	DefaultSchedule,
    Department,
    Employee
)

class DefaultScheduleForm(forms.ModelForm):
	class Meta:
		model = DefaultSchedule
		fields = ['name', 'schedule_time']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'schedule_time': forms.TextInput(attrs={'class': 'form-control'}), 
		}

	def clean_schedule_time(self):
		schedule_time = self.cleaned_data.get('schedule_time')
		
		patt = re.search("^(1[0-2]|[1-9])(a|p)-(1[0-2]|[1-9])(a|p)$", schedule_time)
		if patt:
			time_gaps = schedule_time.split('-')
			if time_gaps[0] == time_gaps[1]:
				raise forms.ValidationError(f'Wrong time gap: "{schedule_time}"') 
		else: raise forms.ValidationError(f'Incorrect format time: "{schedule_time}", corr. example: "11a-9p"')

		return schedule_time

class DepartmentForm(forms.ModelForm):
	class Meta:
		model = Department
		fields = ['name']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'})
		}

class EmployeeForm(forms.ModelForm):
	class Meta:
		model = Employee
		fields = ['name', 'number', 'department']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'number': forms.NumberInput(attrs={'class': 'form-control'}),
			'department': forms.Select(attrs={'class': 'form-select'}),
		}