from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    login_index,
    login,
    logout,
    register,
    activation,
    resend_activation,
    activation_done,
    change_company_name,
    change_username,
)

urlpatterns = [
    path('', login_index, name='login_index'),

    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),

    path('register/', register, name='register'),
    path('register/activation/', activation, name='activation'),
    path('register/activation/resend', resend_activation, name='resend_activation'),
    path('register/<uidb64>/<token>', activation_done, name='activation_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset/password_reset.html'), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset/password_reset_complete.html'), 
     name='password_reset_complete'),

    path('change_company_name/', change_company_name, name='change_company_name'),
    path('change_username/', change_username, name='change_username'),
]
