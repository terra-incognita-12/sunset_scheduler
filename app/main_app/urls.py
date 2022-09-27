from django.urls import path

from .views import (
    index,
    default_schedule_add,
    default_schedule_update,
    default_schedule_delete,
)

urlpatterns = [
    path('', index, name='index'),

    path('default_schdeule/add', default_schedule_add, name='default_schedule_add'),
    path('default_schedule/update', default_schedule_update, name='default_schedule_update'),
    path('default_schedule/delete', default_schedule_delete, name='default_schedule_delete')
]