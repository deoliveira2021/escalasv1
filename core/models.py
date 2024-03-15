# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone

from core.mail import send_mail_template

from pessoal import models as pessoalModel

"""class CourseManager(models.Manager):

    def search(self, query):
        return self.get_queryset().filter(
            models.Q(name__icontains=query) | \
            models.Q(description__icontains=query)
        )
"""
class Escala(models.Model):

    descricao = models.CharField('Descrição', max_length=40)
    ticado = models.BooleanField('Marcado', blank=True, default=True)
    precedencia = models.IntegerField('Precedência',default=0)
    nrmilitaresnaescala = models.IntegerField('Nº Mil na Escala?', null=False, default=3)
    CIRCULO_CHOICES = [ (0, 'Oficial'), (1, 'ST/SGT'),(2, 'CB/SD'), (3, 'TODOS')]
    idcirculo = models.IntegerField('Círculo Hierárquico',null=False,
    choices=CIRCULO_CHOICES, blank=False)
    qtdporescala = models.IntegerField('Qtde por dia',null=False, default=1)
    CORRIDA_CHOICES= [(1, "SIM"), (0, "NÃO")]
    corrida = models.BooleanField('Corrida', choices= CORRIDA_CHOICES, default=0)
    folgaminima = models.IntegerField('Folga Mínima',null=False, default=1)

    #objects = CourseManager()

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Escala'
        verbose_name_plural = 'Escalas'
        ordering = ['precedencia']
"""
    #@models.permalink
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('courses:details', args=[self.slug])

    def release_lessons(self):
        today = timezone.now().date()
        return self.lessons.filter(release_date__gte=today)

"""

# -- Cria a Tabela de controlar folgas
class ControlarFolgas(models.Model):
#    idmilitar = models.ForeignKey(pessoalModel.Militar,
#        verbose_name='Id Militar', related_name='idmilitar',
#        on_delete = models.CASCADE, blank=True, default=0
#        )

    idmilitar = models.IntegerField('Id Militar', blank=True, default=0)
    idcirculo = models.IntegerField('Id Círculo', blank=True, default=-1 )

    #ESCALA_CHOICES=Escala.objects.values_list('id', 'descricao')
    #idescala = models.IntegerField('Escala', blank=False, choices=ESCALA_CHOICES)
    idescala = models.IntegerField('Escala', blank=False)

    red = models.IntegerField('Folga Vermelha', null=True, blank=True, default=100)
    black = models.IntegerField('Folga Preta',  null=True, blank=True, default=100)
    realred = models.IntegerField('Folga Vermelha',  blank=False, default=100)
    realblack = models.IntegerField('Folga Preta', blank=False, default=100)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Folga'
        verbose_name_plural = 'Folgas'
        ordering = ['-id']


# -- Cria a Tabela de designar escalas
class DesignarEscala(models.Model):
    idmilitar = models.IntegerField('Id Militar', blank=True, default=0)
    idcirculo = models.IntegerField('Id Círculo', blank=True, default=0)
    idescala = models.IntegerField('Id Escala', blank=True, default=0)
    preta = models.BooleanField('Preta', blank=True, default=True)
    vermelha = models.BooleanField('Vermelha', blank=True, default=True)
    seg = models.BooleanField('Seg', blank=True, default=True)
    ter = models.BooleanField('Ter', blank=True, default=True)
    qua = models.BooleanField('Qua', blank=True, default=True)
    qui = models.BooleanField('Qui', blank=True, default=True)
    sex = models.BooleanField('Sex', blank=True, default=True)
    sab = models.BooleanField('Sáb', blank=True, default=True)
    dom = models.BooleanField('Dom', blank=True, default=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Designar'
        verbose_name_plural = 'Designados'
        ordering = ['-id']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('core:escalar', args=[self.idmilitar, self.idcirculo])

# -- Cria a Tabela de Dispensas
class Dispensas(models.Model):
    idmilitar = models.IntegerField('Id Militar')
    idcirculo = models.IntegerField('Id Círculo')
    datainicio = models.DateField('Início')
    datafim = models.DateField('Fim')
    motivo = models.CharField('Motivo', max_length=100)
    PREJUZO_CHOICES= [(1, "SIM"), (0, "NÃO")]
    prejuizo = models.BooleanField('Prejuízo da Escala?',
    blank=True, default=True, choices=PREJUZO_CHOICES)

    def __str__(self):
        return str(self.idmilitar)

    class Meta:
        verbose_name = 'Dispensa'
        verbose_name_plural = 'Dispensas'
        ordering = ['idmilitar']

# -- Cria a Tabela de Feriados
class Feriados(models.Model):
    data = models.DateField('Data', null=False, blank=False, max_length=10,)
    descricao = models.CharField('Feriado', max_length=60)
    dia = models.CharField('Dia da Semana', max_length=15, blank = True)

    def __str__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Feriado'
        verbose_name_plural = 'Feriados'
        ordering = ['data']
