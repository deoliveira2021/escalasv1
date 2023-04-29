from django import forms
from .models import *

class FormPrevisao(forms.Form):
    searchEscala = forms.CharField(label= 'Escala', required=False, max_length=40)
    searchMilitar = forms.CharField(label= 'Militar', required=False, max_length=40)

    ##### -- este código dentro dessa área de comentário é o original -- ######
    nome_guerra = forms.CharField(label= 'Nome de Guerra', required=False, max_length=40)
    escala = forms.CharField(label= 'Escala', required=False, max_length=40)
    dataInicio = forms.DateField(label='Início', required=False)
    dataFim = forms.DateField(label='Fim', required=False)
    ##### -- este código dentro dessa área de comentário é o original -- ######


class MilitarEscaladoForm(forms.Form):
    POSTO_CHOICES = [(5, "Cel"), (6, "T Cel"), (7, "Maj"),
        (8, "Cap"), (9, "1º Ten"), (10, "2º Ten"), (11, "Asp"),
        (18, "S Ten"), (19, "1º Sgt"), (20, "2º Sgt"), (21, "3º Sgt"),
        (22, "Cb EP"), (23, "Cb EV"), (24, "SD PQDT EP"), (27, "SD EP"), (28, "SD EV")]
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
