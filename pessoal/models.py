import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
    UserManager)
from django.conf import settings


class Circulo(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField('Círculo', max_length=10)

    def __init__(self):
        return self.descricao

    class Meta:
        verbose_name = 'Circulo'
        verbose_name_plural = 'Circulos'
        ordering = ['-id']

#class Militar(usuarioModel.User):
class Militar(models.Model):
    email = models.EmailField('E-mail', unique=False)
    nome = models.CharField('Nome Completo', max_length=100, null= False, blank=False, default='')
    cpf = models.CharField(
        'CPF', max_length=11, null=True,
        validators=[validators.RegexValidator(re.compile(r"[0-9]"),
            'CPF só pode conter digitos de 0 a 9', 'invalid')],
    )
    nome_guerra = models.CharField('Nome de Guerra', max_length=40, null= False, blank=False, default='')

    CIRCULO_CHOICES = [ (0, 'Oficial'), (1, 'ST/SGT'),
                        (2, 'CB/SD'), (3, 'TODOS')]
    idcirculo = models.IntegerField('Círculo'
        , choices=CIRCULO_CHOICES, blank=False
    )

    #idcirculo = models.ForeignKey(Circulo,
    #verbose_name='idcirculo', related_name='idcirculo',
    #on_delete = models.CASCADE,
    #)
    #o índice começa em 5 aqui para mantar
    #uma correspondência com todos os postos
    #existentes no Exército, assim teríamos
    # 1 - Marechal, 2 - Gen de Exército
    # 3 - Gen de Divisão, 4 - Gen Brigada
    # e os demais, conforme abaixo enumerados:

    #Este código foi comentado em 04FEV24 porque estava dando problema com a numeração dos postos...
    # Postos de acordo com o previsto no contracheque...
    # POSTO_CHOICES = [(5, "Cel"), (6, "T Cel"), (7, "Maj"),
    #     (8, "Cap"), (9, "1º Ten"), (10, "2º Ten"), (11, "Asp"),
    #     (18, "S Ten"), (19, "1º Sgt"), (20, "2º Sgt"), (21, "3º Sgt"),
    #     (22, "Cb EP"), (23, "Cb EV"), (24, "SD PQDT EP"), (27, "SD EP"), (28, "SD EV")]
    
    #Substituiu o código acima, para acertar 
    POSTO_CHOICES = [(5, "Cel"), (6, "T Cel"), (7, "Maj"),
             (8, "Cap"), (9, "1º Ten"), (10, "2º Ten"), (11, "Asp"),
             (12, "S Ten"), (13, "1º Sgt"), (14, "2º Sgt"), (15, "3º Sgt"),
             (16, "Cb"), (17, "SD")]
   


    posto = models.IntegerField('Posto/Graduação', choices = POSTO_CHOICES, blank=False)
    GENDER_CHOICES =((1, "Masculino"), (2, "Feminino"), )
    sexo = models.IntegerField('Gênero', null=True, choices=GENDER_CHOICES, blank=True)
    tel1 = models.CharField('WhatsApp', max_length=15, null=True, blank=True)
    tel2 = models.CharField('Outro número', max_length=15, null=True, blank=True)
    data_nasc = models.DateField('Data Nascimento', null=True, blank=True)
    data_praca = models.DateField('Data de Praça',null=True, blank=True)

    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)

    #militar = usuarioModel.User

    antiguidade = models.IntegerField('Antiguidade', null=False, blank=False, default=1)

    PRONTO_CHOICES= [(0, "NÃO"), (1, "SIM")]
    pronto = models.BooleanField('Pronto?', choices= PRONTO_CHOICES,
    default=1, blank=False, null=True)
    ticado = models.BooleanField('Marcado?', default=True)

    #objects = UserManager()

    #USERNAME_FIELD = 'nome_guerra'
    #REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.nome_guerra

    class Meta:
        verbose_name = 'Militar'
        verbose_name_plural = 'Militares'
        ordering = ['antiguidade', 'posto']