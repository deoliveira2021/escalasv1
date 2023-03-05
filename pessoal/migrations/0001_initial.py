# Generated by Django 3.2.18 on 2023-03-04 23:26

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Circulo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descricao', models.CharField(max_length=10, verbose_name='Círculo')),
            ],
            options={
                'verbose_name': 'Circulo',
                'verbose_name_plural': 'Circulos',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Militar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('nome', models.CharField(default='', max_length=100, verbose_name='Nome Completo')),
                ('cpf', models.CharField(max_length=11, null=True, validators=[django.core.validators.RegexValidator(re.compile('[0-9]'), 'CPF só pode conter digitos de 0 a 9', 'invalid')], verbose_name='CPF')),
                ('nome_guerra', models.CharField(default='', max_length=40, verbose_name='Nome de Guerra')),
                ('idcirculo', models.IntegerField(choices=[(0, 'Oficial'), (1, 'ST/SGT'), (2, 'CB/SD'), (3, 'TODOS')], verbose_name='Círculo')),
                ('posto', models.IntegerField(choices=[(5, 'Cel'), (6, 'T Cel'), (7, 'Maj'), (8, 'Cap'), (9, '1º Ten'), (10, '2º Ten'), (11, 'Asp'), (12, 'S Ten'), (13, '1º Sgt'), (14, '2º Sgt'), (15, '3º Sgt'), (16, 'Cb'), (17, 'SD')], verbose_name='Posto/Graduação')),
                ('sexo', models.IntegerField(blank=True, choices=[(1, 'Masculino'), (2, 'Feminino')], null=True, verbose_name='Gênero')),
                ('tel1', models.CharField(blank=True, max_length=15, null=True, verbose_name='WhatsApp')),
                ('tel2', models.CharField(blank=True, max_length=15, null=True, verbose_name='Outro número')),
                ('data_nasc', models.DateField(blank=True, null=True, verbose_name='Data Nascimento')),
                ('data_praca', models.DateField(blank=True, null=True, verbose_name='Data de Praça')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')),
                ('antiguidade', models.IntegerField(default=1, verbose_name='Antiguidade')),
                ('pronto', models.BooleanField(choices=[(0, 'NÃO'), (1, 'SIM')], default=1, null=True, verbose_name='Pronto?')),
                ('ticado', models.BooleanField(default=True, verbose_name='Marcado?')),
            ],
            options={
                'verbose_name': 'Militar',
                'verbose_name_plural': 'Militares',
                'ordering': ['antiguidade', 'posto'],
            },
        ),
    ]
