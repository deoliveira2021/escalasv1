from django.urls import re_path, include, path
from django.contrib import admin
admin.autodiscover()
from . import views

app_name = 'core'
urlpatterns = [
       re_path(r'^$', views.home, name='home'),
       re_path(r'^escalas/cadastrar', (views.escalas), name='escalas'),
       re_path(r'^escalas/editar/(?P<idescala>\d+)/(?P<pagina>\d+)',
              (views.editar_escala), name='editar_escala'),
       re_path(r'^escalas/excluir/(?P<idescala>\d+)/(?P<pagina>\d+)',
              (views.excluir_escala), name='excluir_escala'),
       re_path(r'^designar/(?P<idmilitar>\d+)/(?P<idcirculo>\d+)',
              (views.escalar), name='escalar'),
       re_path(r'^designar/editar/(?P<iddesignacao>\d+)',
              (views.editar_escalar), name='editar_escalar'),
       re_path(r'^designar/excluir/(?P<iddesignacao>\d+)',
              (views.delete_escalar), name='excluir_designacao'),
       re_path(r'^feriados/cadastrar', (views.feriados), name='feriados'),
       re_path(r'^feriados/editar/(?P<idferiado>\d+)/(?P<pagina>\d+)', (views.editar_feriado),
               name='editar_feriado'),
       re_path(r'^feriados/excluir/(?P<idferiado>\d+)/(?P<pagina>\d+)', (views.excluir_feriado),
               name='excluir_feriado'),
       re_path(r'^dispensa-ferias/(?P<idmilitar>\d+)/(?P<idcirculo>\d+)',
              (views.dispensar), name='dispensar'),
       re_path(r'^dispensa-feria/editar/(?P<iddispensa>\d+)/(?P<pagina>\d+)',
              (views.editar_dispensa), name='editar_dispensa'),
       re_path(r'^dispensa-feria/excluir/(?P<iddispensa>\d+)/(?P<pagina>\d+)',
              (views.excluir_dispensa), name='excluir_dispensa'),

       re_path(r'^admin/', admin.site.urls),
       
#       re_path(r'^listar-escalas', views.index, name='listar'),
       #re_path(r'^contato/$', views.contact, name='contact'),
]
