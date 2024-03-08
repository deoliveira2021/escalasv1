from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from core.mail import send_mail_template
from core.utils import generate_hash_key

from .models import PasswordReset
from pessoal.models import Militar


#import para enviar SMS
#from sms import Message
#import sms

# Import para mandar ler arquivo e mostrar conteúdo no console.
#import pandas as pd
#from IPython.display import display
#

User = get_user_model()


class PasswordResetForm(forms.Form):

    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise forms.ValidationError(
            'Nenhum usuário encontrado com este e-mail'
        )


#*******************************************************************************************************************
#                                       Teoricamente mandaria SMS
#*******************************************************************************************************************
#    with sms.get_connection() as connection:
#        sms.Message(
#            'Here is the message', '+5585996932640', ['+5585996932640'],
#            connection=connection
#        ).send()
#*******************************************************************************************************************

    def save(self):
        user = User.objects.get(email=self.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        template_name = 'password_reset_mail.html'
        subject = 'Criar nova senha no Sistema de Escala de Serviços'
        context = {
            'reset': reset,
        }
        send_mail_template(subject, template_name, context, [user.email])


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de Senha', widget=forms.PasswordInput
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'nome', 'email', 'sexo', 'is_staff', 'posto',
                  'cpf','nome_guerra','tel1', 'tel2','data_nasc','data_praca']
        

class Register_staffForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirmação de Senha', widget=forms.PasswordInput
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('A confirmação não está correta')
        return password2

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = (['username', 'email', 'sexo', 'posto', 'nome', 'nome_guerra',
        'cpf', 'data_nasc','data_praca','tel1', 'tel2',
        'is_active', 'is_staff']
        )


class EditAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (['username', 'email','posto', 'nome', 'nome_guerra',
        'cpf','sexo', 'data_nasc','data_praca','tel1', 'tel2',
        'is_active', 'is_staff']
        )
