from django import forms

#meus imports ....
from .models import Militar

#class SalvarMilitar(forms.ModelForm):
#    pronto = forms.BooleanField(label ='Pronto?', initial=1, required=False)

#    def save(self, commit=True):
#        militar = super(SalvarMilitar, self).save(commit=False)
#        if commit:
#            militar.save()
#        return militar

#    class Meta:

#        model = Militar
#        fields = (['idcirculo','posto', 'antiguidade',
#                    'pronto', 'nome', 'nome_guerra',
#                    'email',  'tel1', 'tel2' ]
#        )
#        fields = (['idcirculo', 'antiguidade', 'pronto',
#        'ticado','email', 'sexo', 'posto', 'nome', 'nome_guerra',
#        'cpf', 'data_nasc','data_praca','tel1', 'tel2',]
#        )


class MilitarForm(forms.ModelForm):
    pronto = forms.BooleanField(label ='Pronto?', initial=1, required=False)
    class Meta:
        model = Militar
        fields = (['idcirculo','posto', 'antiguidade',
                    'pronto', 'nome', 'nome_guerra',
                    'email',  'tel1', 'tel2' ]
        )
