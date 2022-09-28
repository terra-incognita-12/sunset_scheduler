from django.urls import path

from .views import (
    index,

    default_schedule_add,
    default_schedule_update,
    default_schedule_delete,

    department_add,
    department_update,
    department_delete,

    employee_add,
    employee_update,
    employee_delete,
)

urlpatterns = [
    path('', index, name='index'),

    path('default_schdeule/add', default_schedule_add, name='default_schedule_add'),
    path('default_schedule/update', default_schedule_update, name='default_schedule_update'),
    path('default_schedule/delete', default_schedule_delete, name='default_schedule_delete'),

    path('department/add', department_add, name='department_add'),
    path('department/update', department_update, name='department_update'),
    path('department/delete', department_delete, name='department_delete'),

    path('employee/add', employee_add, name='employee_add'),
    path('employee/update', employee_update, name='employee_update'),
    path('employee/delete', employee_delete, name='employee_delete'),
]