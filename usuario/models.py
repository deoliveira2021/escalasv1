import re

from django.db import models
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import quote
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

# imports até o dia 15nov2021
#from django.db import models
#from django.core import validators
#from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin,
#    UserManager)
#from django.conf import settings

class UserManager(BaseUserManager):
    def _create_user(self, username, email, password, is_staff, is_superuser, rank,
        fullname, cpf, tag_name, gender, phone_1, phone_2, birthday, square_date):
        now = timezone.now()
        if not username:
            raise ValueError(_('Nome de usuário deve ser fornecido!'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, is_staff=is_staff,
               is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now,
               rank=rank, fullname=fullname, cpf=cpf, tag_name=tag_name, gender=gender,
               phone_1=phone_1, phone_2=phone_2, birthday=birthday, square_date=square_date)
        user.set_password(password)
        user.save(using=self._db)
        return user
        def create_user(self, username, email=None, password=None, rank=None,
            fullname=None, cpf=None, tag_name=None, gender=None, phone_1=None,
            phone_2=None, birthday=None, square_date=None):
            return self._create_user(username, email, password, False, False, rank,
                fullname, cpf, tag_name, gender, phone_1, phone_2, birthday, square_date)
        def create_superuser(self, username, email, password, rank, fullname,
            cpf, tag_name, gender, phone_1, phone_2, birthday, square_date):
            user=self._create_user(username, email, password, True, True, rank,
                fullname, cpf, tag_name, gender, phone_1, phone_2, birthday, square_date)
            user.is_active=True
            user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Nome de Usuário', max_length=30, unique=True,
        validators=[validators.RegexValidator(re.compile('^[\w.@+-]+$'),
            'O nome de usuário só pode conter letras, digitos ou os '
            'seguintes caracteres: @/./+/-/_', 'invalid')]
    )
    email = models.EmailField('E-mail', unique=True)
    nome = models.CharField('Nome Completo', max_length=100, null=True, blank=True)
    cpf = models.CharField(
        'CPF', max_length=11, null=True,
        validators=[validators.RegexValidator(re.compile(r"[0-9]"),
            'CPF só pode conter digitos de 0 a 9', 'invalid')],
    )
    nome_guerra = models.CharField('Nome de Guerra', null=True, max_length=40, blank=True)

    #o índice começa em 5 aqui para manter
    #uma correspondência com todos os postos
    #existentes no Exército, assim teríamos
    # 1 - Marechal, 2 - Gen de Exército
    # 3 - Gen de Divisão, 4 - Gen Brigada
    # e os demais, conforme abaixo enumerados:
    
    #Este código foi comentado em 04FEV24 porque estava dando problema com a numeração dos postos...
    # POSTO_CHOICES = [(5, "Cel"), (6, "T Cel"), (7, "Maj"),
    #     (8, "Cap"), (9, "1º Ten"), (10, "2º Ten"), (11, "Asp"),
    #     (18, "S Ten"), (19, "1º Sgt"), (20, "2º Sgt"), (21, "3º Sgt"),
    #     (22, "Cb EP"), (23, "Cb EV"), (24, "SD PQDT EP"), (27, "SD EP"), (28, "SD EV")
    # ]

    #Substituiu o código acima, para acertar 
    POSTO_CHOICES = [(5, "Cel"), (6, "T Cel"), (7, "Maj"),
             (8, "Cap"), (9, "1º Ten"), (10, "2º Ten"), (11, "Asp"),
             (12, "S Ten"), (13, "1º Sgt"), (14, "2º Sgt"), (15, "3º Sgt"),
             (16, "Cb"), (17, "SD")]

    posto = models.IntegerField('Posto/Graduação', null=True, choices = POSTO_CHOICES, blank=True)
    GENDER_CHOICES =((1, "Masculino"), (2, "Feminino"), )
    sexo = models.IntegerField('Gênero', null=True, choices=GENDER_CHOICES, blank=True)
    tel1 = models.CharField('Telefone 1', max_length=15, null=True, blank=True)
    tel2 = models.CharField('Telefone 2', max_length=15, null=True, blank=True)
    data_nasc = models.DateField('Data Nascimento', null=True, blank=True)
    data_praca = models.DateField('Data de Praça',null=True, blank=True)
    is_active = models.BooleanField('Ativo?', blank=True, default=True)
    IS_STAFF_CHOICES= [(1, "SIM"), (0, "NÃO")]
    is_staff = models.BooleanField('Adm?', blank=True, default=0, choices=IS_STAFF_CHOICES)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.nome or self.username

    def get_short_name(self):
        return self.username

    def get_full_name(self):
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class PasswordReset(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name='Usuário',
        related_name='resets', on_delete=models.CASCADE,
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)

    def __str__(self):
        return '{0} em {1}'.format(self.user, self.created_at)

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        ordering = ['-created_at']