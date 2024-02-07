from django.urls import re_path, include
from django.contrib import admin
from . import views

app_name = 'pessoal'
urlpatterns = [
      re_path(r'^militar/cadastrar/', (views.cadastrarMilitar), name='cadastrarMilitar'),
      #não está funcinando com o número da página, pesquisar depois
      #re_path(r'^editar-militar/(?P<idmilitar>\d+)+(?P<idcirculo>\d+)+(?P<page>\d+)',
      re_path(r'^militar/editar/(?P<idmilitar>\d+)+(?P<idcirculo>\d+)/(?P<pagina>\d+)',
              (views.editar_militar), name='editar_militar'),

      re_path(r'^(?P<idmilitar>\d+)/(?P<idcirculo>\d+)/(?P<pagina>\d+)',
              (views.delete_militar), name='delete_militar'),

#       re_path(r'^', (views.cadastrarMilitar), name='cadastrarMilitar'),
       #re_path(r'^contato/$', views.contact, name='contact'),
 ]
