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