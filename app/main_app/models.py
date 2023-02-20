from enum import unique
from django.db import models
from django.conf import settings

class DefaultSchedule(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=255, unique=True)
    schedule_time = models.CharField(max_length=8)

    class Meta:
        verbose_name = "Default Schedule"
        verbose_name_plural = "Default Schedules"

    def __str__(self):
        return self.name

class Department(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    name = models.CharField(max_length=255)
    number = models.IntegerField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Employee"
        verbose_name_plural = "Employees"

    def __str__(self):
        return f'{self.name} ({str(self.number)})'

class ScheduleProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    name = models.CharField(max_length=255, unique=True)
    begin_date = models.DateField()

    class Meta:
        verbose_name = "Schedule Profile"
        verbose_name_plural = "Schedule Profiles"

    def __str__(self):
        return self.schedule_name

class CurrentSchedule(models.Model):
    schedule_profile = models.OneToOneField(ScheduleProfile, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Current Schedule"
        verbose_name_plural = "Current Schedules"

    def __str__(self):
        return self.schedule_profile

class ScheduleDetail(models.Model):
    schedule_profile = models.ForeignKey(ScheduleProfile, on_delete=models.CASCADE)

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    mon_time = models.CharField(max_length=8, null=True, blank=True)
    tue_time = models.CharField(max_length=8, null=True, blank=True)
    wed_time = models.CharField(max_length=8, null=True, blank=True)
    thr_time = models.CharField(max_length=8, null=True, blank=True)
    fri_time = models.CharField(max_length=8, null=True, blank=True)
    sat_time = models.CharField(max_length=8, null=True, blank=True)
    sun_time = models.CharField(max_length=8, null=True, blank=True)

    mon_duty = models.CharField(max_length=100, null=True, blank=True)
    tue_duty = models.CharField(max_length=100, null=True, blank=True)
    wed_duty = models.CharField(max_length=100, null=True, blank=True)
    thr_duty = models.CharField(max_length=100, null=True, blank=True)
    fri_duty = models.CharField(max_length=100, null=True, blank=True)
    sat_duty = models.CharField(max_length=100, null=True, blank=True)
    sun_duty = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Schedule Detail"
        verbose_name_plural = "Schedule Details"

    def __str__(self):
        return f"{self.employee}'s schedule"