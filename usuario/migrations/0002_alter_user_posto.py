# Generated by Django 3.2.18 on 2024-02-05 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='posto',
            field=models.IntegerField(blank=True, choices=[(5, 'Cel'), (6, 'T Cel'), (7, 'Maj'), (8, 'Cap'), (9, '1º Ten'), (10, '2º Ten'), (11, 'Asp'), (12, 'S Ten'), (13, '1º Sgt'), (14, '2º Sgt'), (15, '3º Sgt'), (16, 'Cb'), (17, 'SD')], null=True, verbose_name='Posto/Graduação'),
        ),
    ]