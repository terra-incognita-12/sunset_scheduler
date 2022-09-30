from django.urls import path

from .views import (
    index,
    settings,

    default_schedule_add,
    default_schedule_update,
    default_schedule_delete,

    department_add,
    department_update,
    department_delete,

    employee_add,
    employee_update,
    employee_delete,

    schedule_profile_add,
    schedule_profile_update,
    schedule_profile_delete,

    current_schedule_pick,

    schedule_detail_add,
    schedule_detail_update,
    schedule_detail_delete,

    export_schedule
)

urlpatterns = [
    path('', index, name='index'),
    path('settings', settings, name='settings'),

    path('default_schdeule/add', default_schedule_add, name='default_schedule_add'),
    path('default_schedule/update', default_schedule_update, name='default_schedule_update'),
    path('default_schedule/delete', default_schedule_delete, name='default_schedule_delete'),

    path('department/add', department_add, name='department_add'),
    path('department/update', department_update, name='department_update'),
    path('department/delete', department_delete, name='department_delete'),

    path('employee/add', employee_add, name='employee_add'),
    path('employee/update', employee_update, name='employee_update'),
    path('employee/delete', employee_delete, name='employee_delete'),

    path('schedule_profile/add', schedule_profile_add, name='schedule_profile_add'),
    path('schedule_profile/update', schedule_profile_update, name='schedule_profile_update'),
    path('schedule_profile/delete/<int:pk>', schedule_profile_delete, name='schedule_profile_delete'),

    path('current_schedule', current_schedule_pick, name='current_schedule_pick'),

    path('schedule_detail/add', schedule_detail_add, name='schedule_detail_add'),
    path('schedule_detail/update', schedule_detail_update, name='schedule_detail_update'),
    path('schedule_detail/delete', schedule_detail_delete, name='schedule_detail_delete'),

    path('export_schedule/', export_schedule, name='export_schedule'),
]