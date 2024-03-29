# Generated by Django 4.2.10 on 2024-03-12 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoal', '0004_alter_militar_idcirculo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='militar',
            name='idcirculo',
            field=models.IntegerField(choices=[(0, 'Oficial'), (1, 'ST/SGT'), (2, 'CB/SD'), (3, 'TODOS')], verbose_name='Círculo'),
        ),
        migrations.AlterField(
            model_name='militar',
            name='pronto',
            field=models.BooleanField(choices=[(0, 'NÃO'), (1, 'SIM')], default=1, null=True, verbose_name='Pronto'),
        ),
    ]
