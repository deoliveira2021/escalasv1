from django.contrib import admin

# Register your models here.

from usuario.models import User
from core.models import Escala
admin.site.register(User)
admin.site.register(Escala)