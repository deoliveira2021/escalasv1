from django.urls import re_path, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from . import views as usuario_views

app_name = 'usuario'
urlpatterns = [
#       re_path(r'^entrar/$', LoginView.as_view(template_name='new_login.html'), name='login'),
       re_path(r'^entrar/$', LoginView.as_view(template_name='login.html'), name='login'),
       re_path(r'^sair/$', LogoutView.as_view(template_name='previsao.html'), name='logout'),
       re_path(r'^cadastre-se/$', usuario_views.register, name='register'),
       re_path(r'^usuario/$', usuario_views.register_staff, name='register_staff'),
       re_path(r'^nova-senha/$', usuario_views.password_reset, name='password_reset'),
       re_path(r'^confirmar-nova-senha/(?P<key>\w+)/$', usuario_views.password_reset_confirm, name='password_reset_confirm'),
#       re_path(r'^editar/$', accounts_views.edit, name='edit'),
#       re_path(r'^editar-senha/$', accounts_views.edit_password, name='edit_password'),
]
