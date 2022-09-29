from dataclasses import field
import re
from django import forms

from .models import (
	DefaultSchedule,
    Department,
    Employee,
    ScheduleProfile,
    ScheduleDetail
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

class ScheduleProfileForm(forms.ModelForm):
	class Meta:
		model = ScheduleProfile
		fields = ['name', 'begin_date']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'begin_date': forms.DateInput(
				format=('%Y-%m-%d'),
				attrs={'class': 'form-control', 
					'placeholder': 'Select a date',
					'type': 'date'
				}),
		}

class ScheduleDetailForm(forms.ModelForm):
    class Meta:
        model = ScheduleDetail
        exclude = ['schedule_profile']
        widgets = {
            'employee': forms.Select(attrs={'class': 'form-select'}),

            'mon_time': forms.TextInput(attrs={'list': 'mon-list', 'class': 'form-control'}),
			'tue_time': forms.TextInput(attrs={'list': 'tue-list', 'class': 'form-control'}),
			'wed_time': forms.TextInput(attrs={'list': 'wed-list', 'class': 'form-control'}),
			'thr_time': forms.TextInput(attrs={'list': 'thr-list', 'class': 'form-control'}),
			'fri_time': forms.TextInput(attrs={'list': 'fri-list', 'class': 'form-control'}),
			'sat_time': forms.TextInput(attrs={'list': 'sat-list', 'class': 'form-control'}),
			'sun_time': forms.TextInput(attrs={'list': 'sun-list', 'class': 'form-control'}),

            'mon_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'tue_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'wed_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'thr_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'fri_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'sat_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'sun_duty': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        time_list = [
            self.cleaned_data.get('mon_time'),
            self.cleaned_data.get('tue_time'),
            self.cleaned_data.get('wed_time'),
            self.cleaned_data.get('thr_time'),
            self.cleaned_data.get('fri_time'),
            self.cleaned_data.get('sat_time'),
            self.cleaned_data.get('sun_time')
        ]
        duty_list = [
            self.cleaned_data.get('mon_duty'),
            self.cleaned_data.get('tue_duty'),
            self.cleaned_data.get('wed_duty'),
            self.cleaned_data.get('thr_duty'),
            self.cleaned_data.get('fri_duty'),
            self.cleaned_data.get('sat_duty'),
            self.cleaned_data.get('sun_duty')
        ]

        for i in range(len(time_list)):
            if not time_list[i]:
                if duty_list[i]:
                    raise forms.ValidationError(f"Day off can't have duty")
                else: continue
            patt = re.search("^(1[0-2]|[1-9])(a|p)-(1[0-2]|[1-9])(a|p)$", time_list[i])
            if patt:
                time_gaps = time_list[i].split('-')
                if time_gaps[0] == time_gaps[1]:
                    raise forms.ValidationError(f'Wrong time gap: "{time_list[i]}"')
            else:
                raise forms.ValidationError(f'Incorrect format time: "{time_list[i]}", corr. example: "11a-9p"')

        return self.cleaned_data
            
