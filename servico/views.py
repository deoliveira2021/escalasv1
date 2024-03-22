from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import FileResponse


# from .forms import *
from .models import Servicos
from pessoal.models import Militar
from core.views import gerarPDF


# from ..previsao.models import Previsao

def listar_servicos(request, pagina=1, nrporpagina=22, descricao=None, nomeguerra=None):
    sqlmilitar = "SELECT b.id, a.id as idmilitar, a.posto, a.antiguidade,\
    b.nomeguerra, b.folga, b.data, b.dia, b.nomesubstituto, b.vermelha,\
    c.descricao FROM pessoal_militar a, servico_servicos b, core_escala c\
    WHERE a.id=b.idmilitar AND c.id=b.idescala AND a.idcirculo=b.idcirculo\
    "
    servico_list = []
    if (descricao != None) & (descricao != ""):
        if(nomeguerra != None) & (nomeguerra != ""):
            sqlmilitar += "AND c.descricao LIKE %s AND a.nome_guerra LIKE %s ORDER BY b.data DESC,\
            c.precedencia, b.idcirculo, a.antiguidade"
            servico_list = Militar.objects.raw(sqlmilitar, [descricao,nomeguerra])
        else:
            # criterio = descricao+'%'
            sqlmilitar += "AND c.descricao LIKE %s ORDER BY b.data DESC,\
            c.precedencia, b.idcirculo, a.antiguidade"               
            servico_list = Militar.objects.raw(sqlmilitar, [descricao])

    elif (nomeguerra != None) & (nomeguerra != ""):
        # criterio = '%'+nomeguerra+'%'
        sqlmilitar += "AND a.nome_guerra LIKE %s ORDER BY b.data DESC,\
        c.precedencia, b.idcirculo, a.antiguidade"
        servico_list = Militar.objects.raw(sqlmilitar, [nomeguerra])

    else:
        sqlmilitar += " ORDER BY b.data DESC, c.precedencia, b.idcirculo,\
        a.antiguidade"
        servico_list = Militar.objects.raw(sqlmilitar)

    page = request.GET.get('page', pagina)

    paginator = Paginator(servico_list, nrporpagina)
    try:
        escalados = paginator.page(page)
    except PageNotAnInteger:
        escalados = paginator.page(1)
    except EmptyPage:
        escalados = paginator.page(paginator.num_pages)

    return escalados


# @login_required
def servicos(request):
    template_name = 'listar_servicos.html'

    escala = request.GET.get('escala')
    militar = request.GET.get('militar')   

    escalados = listar_servicos(request,1,22,escala,militar)

    context = {'escalados': escalados}

    return render(request, template_name, context)

# função que gera pdf
def GeneratePDF(request):
    sqlmilitar = "SELECT a.id, a.posto, a.codom,a.antiguidade,b.nomeguerra,\
    b.folga,b.data,b.dia, b.folga,c.descricao FROM pessoal_militar a, \
    servico_servicos b, core_escala c WHERE a.id=b.idmilitar AND \
    c.id=b.idescala AND a.idcirculo=b.idcirculo \
    ORDER BY b.data, c.precedencia, b.idcirculo, a.antiguidade"

    titulo = 'RELATÓRIO GERAL DE SERVIÇOS TIRADOS'
    subtitulo = None

    buffer = gerarPDF(request, sqlmilitar,titulo)

    return FileResponse(buffer, as_attachment=True, filename='servicosTirados.pdf')