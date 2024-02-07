from django.urls import re_path, include
from django.contrib import admin
from . import views

app_name = 'servico'
urlpatterns = [
       re_path(r'^$', views.servicos, name='servicos'),
       re_path(r'^imprimr/', (views.GeneratePDF), name='GeneratePDF'),

       #re_path(r'', (views.salvarServico), name='salvarServico'),
       #re_path(r'^contato/$', views.contact, name='contact'),
]
