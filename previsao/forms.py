from django import forms
from .models import *

class FormPrevisao(forms.Form):
    escala = forms.CharField(label= 'Escala', required=False, max_length=40)
    militar = forms.CharField(label= 'Militar', required=False, max_length=40)

    ##### -- este código dentro dessa área de comentário é o original -- ######
    nome_guerra = forms.CharField(label= 'Nome de Guerra', required=False, max_length=40)
    escala = forms.CharField(label= 'Escala', required=False, max_length=40)
    dataInicio = forms.DateField(label='Início', required=False)
    dataFim = forms.DateField(label='Fim', required=False)
    ##### -- este código dentro dessa área de comentário é o original -- ######


class MilitarEscaladoForm(forms.Form):
    POSTO_CHOICES = [(5, "Cel"), (6, "T Cel"), (7, "Maj"),
             (8, "Cap"), (9, "1º Ten"), (10, "2º Ten"), (11, "Asp"),
             (12, "S Ten"), (13, "1º Sgt"), (14, "2º Sgt"), (15, "3º Sgt"),
             (16, "Cb"), (17, "SD")]
    
    posto = forms.ChoiceField(label='Posto/Graduação', choices = POSTO_CHOICES)

    CIRCULO_CHOICES = [ (0, 'Oficial'), (1, 'ST/SGT'),
                        (2, 'CB/SD'), (3, 'TODOS')]
    idcirculo = forms.ChoiceField(label='Círculo', choices=CIRCULO_CHOICES)

    idmilitar = forms.IntegerField()
    nome_guerra = forms.CharField(label='Escalado', required=False, max_length=40)
    idsubstituto = forms.ChoiceField(label='Substituir por')
    nomesubstituto = forms.CharField(label= 'Substituto', required=False, max_length=40)
    searcheEscala = forms.CharField(label= 'Escala', required=False, max_length=40, initial=None)
    searcheMilitar = forms.CharField(label= 'Militar', required=False, max_length=40, initial=None)
    data = forms.DateField(label='Data do Serviço')
