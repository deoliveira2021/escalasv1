from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import (UserCreationForm, PasswordChangeForm,
    SetPasswordForm)
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from core.utils import generate_hash_key
from django.http import HttpResponse

from .forms import RegisterForm, Register_staffForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset
from pessoal.models import Militar
from pessoal.views import definirCirculo

## - Método para cadastrar militar, a partir do cadastro de usuário.
def cadastrarMilitar(request, militar):
    cpf         = militar[0][1]
    circulo     = definirCirculo(militar[1][1])
    posto       = militar[1][1]
    nome        = militar[2][1]
    nome_guerra = militar[3][1]
    sexo        = militar[4][1]
    email       = militar[5][1]
    tel1        = militar[6][1]
    data_nasc   = militar[7][1]
    data_praca  = militar[8][1]
    insertMilitar = Militar(cpf = cpf, idcirculo = circulo, posto = posto, nome = nome, 
                        nome_guerra = nome_guerra, sexo = sexo, email=email, 
                        tel1=tel1, data_nasc=data_nasc, data_praca=data_praca)
    try:
        insertMilitar.save()
        return HttpResponse('Militar Cadastrado com Sucesso!')
    finally:   
        return HttpResponse('Erro ao tentar cadastrar Militar!')
    


User = get_user_model()

def listar_usuarios(request, pagina=1):
    usuario_list = User.objects.all()

    page = request.GET.get('page', pagina)

    paginator = Paginator(usuario_list, 20)
    try:
        usuarios = paginator.page(page)
    except PageNotAnInteger:
        usuarios = paginator.page(1)
    except EmptyPage:
        usuarios = paginator.page(paginator.num_pages)

    return usuarios

def register(request):
    template_name = 'register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            #pega dados do militar para salvar na tabela militar.
            militar = [
                ('cpf', form.cleaned_data['cpf']),
                ('posto', form.cleaned_data['posto']),
                ('nome', form.cleaned_data['nome']),
                ('nome_guerra', form.cleaned_data['nome_guerra']),
                ('sexo', form.cleaned_data['sexo']),
                ('email', form.cleaned_data['email']),
                ('tel1', form.cleaned_data['tel1']),
                ('data_nasc', form.cleaned_data['data_nasc']),
                ('data_praca', form.cleaned_data['data_praca']),
            ]   
            #chama o método que vai cadastrar o militar com os dados do usuário.
            cadastrarMilitar(request, militar)         
            #Salva o usuário.
            user = form.save()

            ########### Código usado para autenticar o usuário. ###############
            user = authenticate(
                username=user.username, password=form.cleaned_data['password1']
            )
            login(request, user)
            ###################################################################

            return redirect('core:home')
            # return redirect('usuario:register')
    else:
        form = RegisterForm()
    context = {
        'form': form
    }

    usuarios = listar_usuarios(request)
    context = {'form': form, 'usuarios': usuarios}

    return render(request, template_name, context)

def register_staff(request):
    template_name = 'register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            #return redirect('core:home')
            return redirect('usuario:register_staff')
    else:
        form = Register_staffForm()
    context = {
        'form': form
    }
    usuarios = listar_usuarios(request)
    context = {'form': form, 'usuarios': usuarios}
    return render(request, template_name, context)

def password_reset(request):
    template_name = 'password_reset.html'
    context = {}
    form = PasswordResetForm(request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)

def password_reset_confirm(request, key):
    template_name = 'password_reset_confirm.html'
    context = {}
    reset = get_object_or_404(PasswordReset, key=key)
    form = SetPasswordForm(user=reset.user, data=request.POST or None)
    if form.is_valid():
        form.save()
        context['success'] = True
    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit(request):
    template_name = 'edit.html'
    context = {}
    if request.method == 'POST':
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Os dados da sua conta foram alterados com sucesso'
            )
            return redirect('accounts:dashboard')
    else:
        form = EditAccountForm(instance=request.user)
    context['form'] = form
    return render(request, template_name, context)

@login_required
def edit_password(request):
    template_name = 'edit_password.html'
    context = {}
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)
    context['form'] = form
    return render(request, template_name, context)