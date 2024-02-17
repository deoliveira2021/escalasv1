from django import forms
from django.db import models

#import para formatar os campos data
from django.contrib.admin import widgets


#meus imports ....
from .models import *

class escalasForm(forms.ModelForm):

    corrida = forms.BooleanField(label ='Escala Corrida?', required=False)

    def save(self, commit=True):
        escala = super(escalasForm, self).save(commit=False)
        if commit:
            escala.save()
        return escala

    class Meta:
        model = Escala
        fields = (['idcirculo', 'descricao', 'precedencia',
        'folgaminima', 'qtdporescala', 'corrida']
        )

class SalvarFolgas(forms.ModelForm):

    ESCALA_CHOICES= [(-1,'Selecione uma escala')]
    ESCALA_CHOICES+=Escala.objects.values_list('id', 'descricao')
    print("Passou em salvar folgas")
    idescala = forms.ChoiceField(label='Escala', required=True, initial=-1, choices=ESCALA_CHOICES)

    def save (self, commit=True):
        folgas = super(SalvarFolgas, self).save(commit=False)
        if (commit):
            folgas.save()

        return folgas

    class Meta:
        model = ControlarFolgas
        fields = (['idmilitar', 'idcirculo', 'idescala',
        'red', 'realred', 'black', 'realblack']
        )

class SalvarDesignacao(forms.ModelForm):
    def save(self, commit=True):
        designacao = super(SalvarDesignacao, self).save(commit=False)
        if commit:
            designacao.save()
        return designacao

    class Meta:
        model = DesignarEscala
        fields = (['idcirculo', 'idmilitar', 'idescala',
        'preta', 'vermelha', 'seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']
        )


class SalvarDispensa(forms.ModelForm):
    def save(self, commit=True):
        dispensa = super(SalvarDispensa, self).save(commit=False)
        if commit:
            dispensa.save()
        return dispensa

    class Meta:
        model = Dispensas
        fields = (['idcirculo', 'idmilitar', 'datainicio',
        'datafim', 'motivo', 'prejuizo']
        )

#edita a escala
class EditarEscalaForm(forms.ModelForm):
    corrida = forms.BooleanField(label ='Escala Corrida?',
                required=False)

    class Meta:
        model = Escala
        fields = (['idcirculo', 'descricao', 'precedencia',
        'folgaminima', 'qtdporescala', 'corrida']
        )

#Classe para Criar, Editar e excluir dispensas!
class DispensaForm(forms.ModelForm):
    prejuizo = forms.BooleanField(label ='Prejuízo da Escala?',
               required=False, initial=True)

    class Meta:
        model = Dispensas
        fields = (['idcirculo', 'idmilitar', 'datainicio',
        'datafim', 'motivo', 'prejuizo']
        )

#Classe que cria uma instancia de formulário para Cadastrar, Editar ou excluir
#feriados.
class feriadosForm(forms.ModelForm):
    def save(self, commit=True):
        feriado = super(feriadosForm, self).save(commit=False)
        if commit:
            feriado.save()
        return feriado
    class Meta:
        model = Feriados
        fields = (['data', 'descricao', 'dia'])

#editar designação
class EditarDesignacaoForm(forms.ModelForm):
    class Meta:
        model = DesignarEscala
        fields = (['idcirculo', 'idmilitar', 'idescala',
        'preta', 'vermelha', 'seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']
        )

#Editar folgas
class EditarFolgas(forms.ModelForm):
    class Meta:
        model = ControlarFolgas
        fields = (['idmilitar', 'idcirculo', 'idescala',
        'red', 'realred', 'black', 'realblack']
        )

class DeleteDesignacaoForm(forms.ModelForm):
    class Meta:
        model = DesignarEscala
        fields = (['idcirculo', 'idmilitar', 'idescala',
        'preta', 'vermelha', 'seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']
        )

class DeleteFolgas(forms.ModelForm):
    class Meta:
        model = ControlarFolgas
        fields = (['idmilitar', 'idcirculo', 'idescala',
        'red', 'realred', 'black', 'realblack']
        )