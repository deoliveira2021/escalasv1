from django.shortcuts import render, redirect

#meus imports
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import *
from .models import Militar
from core.models import *

@login_required
#def listar_militares(request, pag=None): não funcionou passando a página
def listar_militares(request, pagina=1):
    militar_list = Militar.objects.all()

    #if pag == None:
    page = request.GET.get('page', pagina)

    #page = request.GET.get('page', pag)

    paginator = Paginator(militar_list, 20)
    try:
        militares = paginator.page(page)
    except PageNotAnInteger:
        militares = paginator.page(1)
    except EmptyPage:
        militares = paginator.page(paginator.num_pages)

    return militares

@login_required
def cadastrarMilitar(request):
    template_name = 'cadastrarpessoal.html'
    if request.method == 'POST':
        form = MilitarForm(request.POST)
        if form.is_valid():
            militar = form.save()
            return redirect('pessoal:cadastrarMilitar')
    else:
        form = MilitarForm()

    context = {
        'form': form
    }

    militares = listar_militares(request)
    context = {'form': form, 'militares': militares}

    return render(request, template_name, context)

@login_required
#def editar_militar(request,idmilitar,idcirculo, pagina=1):
def editar_militar(request,idmilitar,idcirculo, pagina):
    sqlmilitar = Militar.objects.filter(id=idmilitar, idcirculo=idcirculo)
    template_name = 'editar_pessoal.html'
    context = {}
    if request.method == 'POST':
        form = MilitarForm(request.POST, instance=sqlmilitar[0])
        if form.is_valid():
            form.save()
            #a mensagem não ficou legal, por isso comentei!
            #messages.success(
            #    request, 'Os dados da sua conta foram alterados com sucesso'
            #)
            return redirect('pessoal:cadastrarMilitar')
    else:
        form = MilitarForm(instance=sqlmilitar[0])

    militares = listar_militares(request, pagina)
    context = {'form': form, 'militares': militares}

    return render(request, template_name, context)

@login_required
def delete_militar(request, idmilitar, idcirculo, pagina):
    queryset = Militar.objects.filter(id=idmilitar)

    #escalas = Escala.objects.all().filter(idcirculo=idcirculo)

    queryset_designar = DesignarEscala.objects.filter(idmilitar=idmilitar,
                  idcirculo=idcirculo)
    queryset_folgas = ControlarFolgas.objects.filter(idmilitar=idmilitar,
                  idcirculo=idcirculo)

    template_name = 'excluir_militar.html'
    context = {}

    if request.method == 'POST':
        if(queryset.count()>0):
            queryset.delete()
            if(queryset_designar.count()>0):
                queryset_designar.delete()

            if(queryset_folgas.count()>0):
                queryset_folgas.delete()

        return redirect('pessoal:cadastrarMilitar')
    else:
        form = MilitarForm(instance=queryset[0])

    militares = listar_militares(request, pagina)
    context = {'form': form, 'militares': militares}

    return render(request, template_name, context)