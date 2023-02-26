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

            'day_1_time': forms.TextInput(attrs={'list': 'day_1-list', 'class': 'form-control'}),
			'day_2_time': forms.TextInput(attrs={'list': 'day_2-list', 'class': 'form-control'}),
			'day_3_time': forms.TextInput(attrs={'list': 'day_3-list', 'class': 'form-control'}),
			'day_4_time': forms.TextInput(attrs={'list': 'day_4-list', 'class': 'form-control'}),
			'day_5_time': forms.TextInput(attrs={'list': 'day_5-list', 'class': 'form-control'}),
			'day_6_time': forms.TextInput(attrs={'list': 'day_6-list', 'class': 'form-control'}),
			'day_7_time': forms.TextInput(attrs={'list': 'day_7-list', 'class': 'form-control'}),

            'day_1_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'day_2_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'day_3_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'day_4_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'day_5_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'day_6_duty': forms.TextInput(attrs={'class': 'form-control'}),
			'day_7_duty': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        time_list = [
            self.cleaned_data.get('day_1_time'),
            self.cleaned_data.get('day_2_time'),
            self.cleaned_data.get('day_3_time'),
            self.cleaned_data.get('day_4_time'),
            self.cleaned_data.get('day_5_time'),
            self.cleaned_data.get('day_6_time'),
            self.cleaned_data.get('day_7_time')
        ]
        duty_list = [
            self.cleaned_data.get('day_1_duty'),
            self.cleaned_data.get('day_2_duty'),
            self.cleaned_data.get('day_3_duty'),
            self.cleaned_data.get('day_4_duty'),
            self.cleaned_data.get('day_5_duty'),
            self.cleaned_data.get('day_6_duty'),
            self.cleaned_data.get('day_7_duty')
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