from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# importar date para usar a função weekday para sar o dia da Semana
from datetime import datetime
from django.conf import settings

#usado para fazer uma conexão direta com o banco de dados
#from django.db import connection #esse método foi comentado pq nãoe está mais usando sql puro

from itertools import chain
from operator import attrgetter
from collections import defaultdict
from itertools import islice



from .forms import *
from .models import *
from pessoal.models import Militar


def home(request):
    return redirect('previsao:previsao') # redireciona para a previsão

def obterMes(data):
    MESES = [
        'JANEIRO',
        'FEVEREIRO',
        'MARÇO',
        'ABRIL',
        'MAIO',
        'JUNHO',
        'JULHO',
        'AGOSTO',
        'SETEMBRO',
        'OUTUBRO',
        'NOVEMBRO',
        'DEZEMBRO',
    ]
    mesNumerico = data.month-1
    mes = MESES[mesNumerico]
    return mes

def nomeDiaSemana(data):
    DIAS = [
        'Segunda-feira',
        'Terça-feira',
        'Quarta-feira',
        'Quinta-feira',
        'Sexta-feira',
        'Sábado',
        'Domingo'
    ]
    #pega o dia numérico da semana
    weekday_numeric = data.weekday()
    #atribui o dia da semana da lista DIAS
    dia = DIAS[weekday_numeric]

    return dia

def gerarRodape(request,p,y):
    p.drawString(30,y-12, 'Usuário: '+request.user.username)
    p.drawCentredString(300, y-12, ' Página: ' + str(p.getPageNumber()))
    p.drawRightString(555,y-12, ' Data: '+ datetime.now().strftime("%d/%m/%Y"))
    return True

@login_required
def gerarPDF(request, sql, titulo, nomeArquivo, subtitulo=None):
    from previsao.views import vermelha
    import io
    from django.shortcuts import HttpResponse   
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
    from reportlab.lib.styles import (ParagraphStyle, getSampleStyleSheet)
    from reportlab.lib import colors

    previsao_list = Militar.objects.raw(sql)

    data = previsao_list[0].data
    nome_mes = obterMes(data)
    
    # Cria um buffer para "salvar" o pdf no buffer para depois ser retornado com um response.
    buffer = io.BytesIO()
    
    #Cria uma lista vazia, depois vai adicionando listas, para passar como parâmetro para função   
    dados = []
    dados.append(['Data', 'Dia da Semana','Escala', 'Posto/Grad', 'Nome', 'OM'])

    style=[
        ('GRID',(0,0),(-1,0),0.75,colors.black), #gera um grid todo fechado
        ('INNERGRID',(0,1),(-1,-1),0.75,colors.black), #gera as linhas do grid sem as bordas das páginas
        ]

    nrlinhas = 1
    nrRegAtual = 0
    nrRegPorData = 0
    for escalado in previsao_list:
        if (nrRegAtual==0 and escalado.data == data):
            dados.append([escalado.data.strftime("%d/%m/%Y"),escalado.dia,escalado.descricao,(escalado.get_posto_display()),escalado.nomeguerra, escalado.get_codom_display()])
            nrRegAtual +=1
        elif(nrRegAtual!=0 and escalado.data == data):
            dados.append(['','',escalado.descricao,(escalado.get_posto_display()),escalado.nomeguerra, escalado.get_codom_display()])

        if(vermelha(data)):
            style.append(('BACKGROUND',(0,nrlinhas-1),(-1,nrlinhas-1),colors.pink))

        if (escalado.data != data):
            style.append(('SPAN',(0,nrlinhas-nrRegPorData),(0,nrlinhas-1)))
            style.append(('VALIGN',(0,nrlinhas-nrRegPorData),(0,nrlinhas-1),'MIDDLE'))            
            
            style.append(('SPAN',(1,nrlinhas-nrRegPorData),(1,nrlinhas-1)))
            style.append(('VALIGN',(1,nrlinhas-nrRegPorData),(1,nrlinhas-1),'MIDDLE'))
            data = escalado.data
            dados.append([escalado.data.strftime("%d/%m/%Y"),escalado.dia,escalado.descricao,(escalado.get_posto_display()),escalado.nomeguerra, escalado.get_codom_display()])
            nrRegAtual +=1
            nrRegPorData = 0
        nrlinhas +=1
        nrRegPorData +=1
    
    # ----------------- Usado para fazer o merge da última escala -----------------
    if (nrlinhas >=1 and nrRegPorData >0):
            style.append(('SPAN',(0,nrlinhas-nrRegPorData),(0,nrlinhas-1)))
            style.append(('VALIGN',(0,nrlinhas-nrRegPorData),(0,nrlinhas-1),'MIDDLE'))            
            
            style.append(('SPAN',(1,nrlinhas-nrRegPorData),(1,nrlinhas-1)))
            style.append(('VALIGN',(1,nrlinhas-nrRegPorData),(1,nrlinhas-1),'MIDDLE'))   
            style.append(('LINEBELOW', (0,-1), (-1,-1), 0.75, colors.black))     
    # -----------------------------------------------------------------
  
    table = Table(dados,rowHeights=25,style=style,repeatRows=1)

    pdf = SimpleDocTemplate(buffer, rightMargin=30,
                            leftMargin=30, topMargin=30, bottomMargin=30)
       
    elements = []
    styleSheet = getSampleStyleSheet()

    # ----------------- Escreve o Título do relatório -----------------
    tituloEstilo = ParagraphStyle('Titulo',
                            fontName="Helvetica-Bold",
                            fontSize=12,
                            parent=styleSheet['Heading2'],
                            alignment=1,
                            spaceAfter=0)

    P = Paragraph(titulo.upper(), tituloEstilo)
    elements.append(P)
    # -----------------------------------------------------------------

    # ---------------- Escreve o Subtítulo do relatório ---------------
   
    if (subtitulo !=None): 
        tituloEstilo = ParagraphStyle('Titulo',
                            fontName="Helvetica-Bold",
                            fontSize=12,
                            parent=styleSheet['Heading1'],
                            alignment=1,
                        spaceAfter=0) 
        subtitulo += nome_mes + ' ' + str(data.year)
        P = Paragraph(subtitulo.upper(), tituloEstilo)
        elements.append(P)
    # -----------------------------------------------------------------

    # Estilo da tabela
    style = TableStyle([
                        # ('BACKGROUND', (0, 0), (-1, 0), (0.2, 0.4, 0.6)),  # Cor de fundo para cabeçalho
                        ('BACKGROUND', (0, 0), (-1, 0), colors.olivedrab),  # Cor de fundo para cabeçalho
                        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),  # Cor do texto no cabeçalho
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento central
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinhamento central                        
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')])  # Fonte negrito para cabeçalho

    table.setStyle(style)

    elements.append(table)
    rodape = 'Relatório gerado por: '+request.user.username
    rodape += '                        em: ' + datetime.now().strftime("%d/%m/%Y")

    estiloRodape = ParagraphStyle('Rodapé',
                            fontName="Helvetica",
                            fontSize=10,
                            alignment=4,
                            spaceAfter=10)
      
    P = Paragraph(rodape, estiloRodape)
    elements.append(P)

    pdf.build(elements)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename='+nomeArquivo
    response.write(buffer.getvalue())
    buffer.close()

    return response



def podeDesignar(idmilitar,idescala,idcirculo):
    #verifica se o militar já está concorrendo a essa escala, se já estiver, não cadastra novamente
    podedesignar = not (DesignarEscala.objects.filter(idmilitar=idmilitar,idcirculo=idcirculo, idescala=idescala).exists())
       
    return (podedesignar)

@login_required
def listar_designacao(request, idmilitar, idcirculo):
    queryset = DesignarEscala.objects.raw('''SELECT DISTINCT(a.idmilitar), a.*,
        b.realblack, b.realred, c.descricao, c.precedencia
        FROM core_designarescala a, core_controlarfolgas b,
        core_escala c WHERE a.idmilitar =%s AND a.idcirculo =%s
        AND b.idmilitar=a.idmilitar AND b.idcirculo=a.idcirculo AND
        b.idescala=a.idescala AND c.id=a.idescala
        ORDER BY c.precedencia''', [idmilitar, idcirculo])

    page = request.GET.get('page', 1)

    #paginator = Paginator(result_list, 8)
    paginator = Paginator(queryset, 24)
    try:
        designacao = paginator.page(page)
    except PageNotAnInteger:
        designacao = paginator.page(1)
    except EmptyPage:
        designacao = paginator.page(paginator.num_pages)

    return designacao

@login_required
def escalar(request, idmilitar=None, idcirculo=None):
    militar = get_object_or_404(Militar, id=idmilitar, idcirculo=idcirculo)
    escalas = Escala.objects.all().filter(idcirculo=idcirculo)

    template_name = 'designarescalas.html'

    if request.method == 'POST':
        form_designacao = SalvarDesignacao(request.POST)
        form_folgas = SalvarFolgas(request.POST)
        if form_designacao.is_valid() & form_folgas.is_valid():
            # designado = form_designacao.save()

            idmilitar = form_designacao.cleaned_data['idmilitar']
            idcirculo = form_designacao.cleaned_data['idcirculo']
            idescala = form_designacao.cleaned_data['idescala']
            red = form_folgas.cleaned_data['realred']
            black = form_folgas.cleaned_data['realblack']
            if podeDesignar(idmilitar,idescala,idcirculo):
                designado = form_designacao.save()
                folgas = ControlarFolgas(idmilitar=idmilitar, idcirculo=idcirculo,
                idescala=idescala, red=red, black=black, realred=red,
                realblack=black)
                folgas.save()

            return redirect('core:escalar', idmilitar, idcirculo)
    else:
        print("passou em escalar")
        form_designacao = SalvarDesignacao()
        form_folgas = SalvarFolgas()

    context = {
        'form_designacao': form_designacao, 'form_folgas':form_folgas,
    }

    escalado_em = listar_designacao(request, idmilitar, idcirculo)
    context = {'form_designacao': form_designacao, 'form_folgas':form_folgas,
                'militar': militar, 'escalas':escalas,
                'escalado_em': escalado_em
    }

    return render(request, template_name, context)

@login_required
def editar_escalar(request, iddesignacao):
    queryset = DesignarEscala.objects.filter(id=iddesignacao)
    idmilitar = queryset[0].idmilitar
    idcirculo = queryset[0].idcirculo
    idescala = queryset[0].idescala
    militar = get_object_or_404(Militar, id=idmilitar, idcirculo=idcirculo)
    
    #adicionado em 14FEV24
    escalas = Escala.objects.all().filter(idcirculo=idcirculo)
    
    queryset_folgas = ControlarFolgas.objects.filter(idmilitar=idmilitar,
                      idcirculo=idcirculo, idescala=idescala)

    red = queryset_folgas[0].realred
    black = queryset_folgas[0].realblack
    queryset_folgas.update(red=red, black=black)

    template_name = 'editar_designacao.html'

    context = {}

    if request.method == 'POST':
        form_designacao = EditarDesignacaoForm(request.POST, instance=queryset[0])
        form_folgas = EditarFolgas(request.POST, instance=queryset_folgas[0])
        if form_designacao.is_valid() & form_folgas.is_valid():
            form_designacao.save()
            form_folgas.save()
            #a mensagem não ficou legal, por isso comentei!
            #messages.success(
            #    request, 'Os dados da sua conta foram alterados com sucesso'
            #)
            return redirect('core:escalar', idmilitar, idcirculo)
    else:
        form_designacao = EditarDesignacaoForm(instance=queryset[0])
        form_folgas = EditarFolgas(instance=queryset_folgas[0])

    escalado_em = listar_designacao(request, idmilitar, idcirculo)
    idescala = queryset[0].idescala

    list_escalas = []
    nome_escala = Escala.objects.filter(id=idescala).last().descricao
    list_escalas = {'id': iddesignacao, 'nome': nome_escala}
    context = {'form_designacao': form_designacao, 'form_folgas':form_folgas,
                'militar': militar, 'escalas':escalas,
                'escalado_em': escalado_em, 'lista_escalas':list_escalas,
    }

    return render(request, template_name, context)

@login_required
def delete_escalar(request, iddesignacao):
    queryset = DesignarEscala.objects.filter(id=iddesignacao)
    idmilitar = queryset[0].idmilitar
    idcirculo = queryset[0].idcirculo
    idescala = queryset[0].idescala
    militar = get_object_or_404(Militar, id=idmilitar, idcirculo=idcirculo)

    queryset_folgas = ControlarFolgas.objects.filter(idmilitar=idmilitar,
                      idcirculo=idcirculo, idescala=idescala)

    template_name = 'excluir_designacao.html'

    if request.method == 'POST':
        if queryset.exists():
            if queryset_folgas.exists():
                queryset_folgas.delete()
            
            queryset.delete()
            return redirect('core:escalar', idmilitar, idcirculo)
    else:
        form_designacao = DeleteDesignacaoForm(instance=queryset[0])
        form_folgas = DeleteFolgas(instance=queryset_folgas[0])


    context = {'form_designacao': form_designacao, 'form_folgas':form_folgas,
                'militar': militar,
    }

    return render(request, template_name, context)

#método que retorna uma lista com as escalas para preencher a tabela do form
@login_required
def listar_escalas(request, pagina=1):
    escala_list = Escala.objects.all()
    page = request.GET.get('page', pagina)

    paginator = Paginator(escala_list, 24)
    try:
        escalas = paginator.page(page)
    except PageNotAnInteger:
        escalas = paginator.page(1)
    except EmptyPage:
        escalas = paginator.page(paginator.num_pages)

    return escalas

@login_required
def escalas(request):
    template_name = 'cadastrarescalas.html'
    if request.method == 'POST':
        form = escalasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:escalas')
    else:
        form = escalasForm()

    context = {
        'form': form
    }

    escalas = listar_escalas(request)
    context = {'form': form, 'escalas': escalas}

    return render(request, template_name, context)

@login_required
def editar_escala(request,idescala, pagina):
    queryset = Escala.objects.filter(id=idescala)
    template_name = 'editar_escala.html'
    context = {}
    if request.method == 'POST':
        form = escalasForm(request.POST, instance=queryset[0])
        if form.is_valid():
            form.save()
            return redirect('core:escalas')
    else:
        form = escalasForm(instance=queryset[0])

    escalas = listar_escalas(request, pagina)
    context = {'form': form, 'escalas': escalas}

    return render(request, template_name, context)

@login_required
def excluir_escala(request,idescala, pagina):
    queryset = Escala.objects.filter(id=idescala)
    if (queryset.count()==0):
        return redirect('core:escalas')
    template_name = 'excluir_escala.html'
    if request.method == 'POST':
        queryset_designacao = DesignarEscala.objects.filter(idescala=idescala)
        queryset_folgas = ControlarFolgas.objects.filter(idescala=idescala)
        if (queryset.count()>0):
            if queryset_designacao.count()>0:
                queryset_designacao.delete() #Excluir toda as designações dessa escala
            if queryset_folgas.count()>0:
                queryset_folgas.delete() # Exclui todas as folgas dessa escala
            queryset.delete()
            return redirect('core:escalas')
    else:
        form = escalasForm(instance=queryset[0])

    escalas = listar_escalas(request, pagina)
    context = {'form': form, 'escalas': escalas}

    return render(request, template_name, context)
# método que retorna os feriados para preencher a tabela no formulário
@login_required
def listar_feriados(request, pagina=1):
    feriados_list = Feriados.objects.all()
    page = request.GET.get('page', pagina)

    paginator = Paginator(feriados_list, 20)
    try:
        feriados = paginator.page(page)
    except PageNotAnInteger:
        feriados = paginator.page(1)
    except EmptyPage:
        feriados = paginator.page(paginator.num_pages)

    return feriados

@login_required
def feriados(request):
    template_name = 'cadastrarferiados.html'
    if request.method == 'POST':
        data = datetime.strptime(request.POST.get('data'),'%Y-%m-%d')
        #data = request.POST.get('data')
        descricao = request.POST.get('descricao')
        dia  = nomeDiaSemana(data)
        dados = {'data': data, 'dia': dia, 'descricao': descricao}

        form = feriadosForm(dados)
        #form = feriadosForm(request.POST)
        if form.is_valid():
            feriado = form.save()
            return redirect('core:feriados')
    else:
        form = feriadosForm()

    context = {
        'form': form
    }

    feriados = listar_feriados(request)
    context = {'form': form, 'feriados': feriados}

    return render(request, template_name, context)

@login_required
def editar_feriado(request,idferiado, pagina):
    queryset = Feriados.objects.filter(id=idferiado)
    template_name = 'editar_feriado.html'
    context = {}
    if request.method == 'POST':
        data = datetime.strptime(request.POST.get('data'), "%d/%m/%Y")
        descricao = request.POST.get('descricao')
        dia  = nomeDiaSemana(data)
        dados = {'data': data, 'dia': dia, 'descricao': descricao}

#        form = EditarFeriadosForm(request.POST, instance=queryset[0])
        #aqui os dados  foram complementados e passados para criar o Objeto
        #feriadosForm, que anter estava sendo criado apenas com os dados do
        #request.POST
        form = feriadosForm(dados, instance=queryset[0])
        if form.is_valid():
            form.save()
            return redirect('core:feriados')
    else:
        form = feriadosForm(instance=queryset[0])

    feriados = listar_feriados(request, pagina)
    context = {'form': form, 'feriados': feriados}

    return render(request, template_name, context)

@login_required
def excluir_feriado(request,idferiado, pagina):
    queryset = Feriados.objects.filter(id=idferiado)
    template_name = 'excluir_feriado.html'
    context = {}
    if request.method == 'POST':
        form = feriadosForm(request.POST, instance=queryset[0])
        if form.is_valid():
            queryset.delete()
            return redirect('core:feriados')
    else:
        form = feriadosForm(instance=queryset[0])

    feriados = listar_feriados(request, pagina)
    context = {'form': form, 'feriados': feriados}

    return render(request, template_name, context)

# método que retorna as dispenss de um militar para preencher a tabela
@login_required
def listar_dispensas(request, idmilitar, idcirculo, pagina=1):
    # se estiver em modo debug, utilizamos o banco sqlite, caso contrário, utilizamos o PostgreSQL.
#   if settings.DEBUG:
#       #este código só funciona em sqlite
#          queryset = '''SELECT *, (julianday(datafim) - julianday(datainicio)+1) AS 'dias'
#              FROM core_dispensas WHERE idmilitar =%s AND idcirculo =%s
#              ORDER BY datainicio'''
#   else:

    # este código só funciona em PostgreSQL, soma 1 para poder contar o dia do fim
    # o argumento int é para voltar número sem vírgula
    queryset = '''SELECT *, EXTRACT(day FROM(AGE(datafim+1, datainicio))):: int AS dias
           FROM core_dispensas WHERE idmilitar =%s AND idcirculo =%s
           ORDER BY datainicio'''


      #este código só funciona em mysql
    # queryset = '''SELECT *, DATEDIFF (datafim+1,datainicio) AS 'dias'
    #     FROM core_dispensas WHERE idmilitar =%s AND idcirculo =%s
    #     ORDER BY datainicio'''

    

    dispensas = Dispensas.objects.raw(queryset, [idmilitar, idcirculo])
    page = request.GET.get('page', pagina)

    paginator = Paginator(dispensas, 8)
    try:
        dispensas = paginator.page(page)
    except PageNotAnInteger:
        dispensas = paginator.page(1)
    except EmptyPage:
        dispensas = paginator.page(paginator.num_pages)

    return dispensas

@login_required
def dispensar(request, idmilitar=None, idcirculo=None):
    militar = get_object_or_404(Militar, id=idmilitar, idcirculo=idcirculo)
    template_name = 'cadastrardispensas.html'
    if request.method == 'POST':
        form_dispensa = DispensaForm(request.POST)
        if form_dispensa.is_valid():
            designado = form_dispensa.save()

            return redirect('core:dispensar', idmilitar, idcirculo)
    else:
        form_dispensa = DispensaForm()

    context = {
        'form': form_dispensa,
    }

    disp_list = listar_dispensas(request, idmilitar, idcirculo)
    context = {'form': form_dispensa,
                'militar': militar,
                'dispensado': disp_list
    }

    return render(request, template_name, context)

@login_required
def editar_dispensa(request, iddispensa, pagina):
    queryset = Dispensas.objects.filter(id=iddispensa)
    #se não tiver dispensas retorna à tela principal das dispensas
    if (queryset.count()==0):
        return redirect('core:dispensar')

    #pega o id do militar e do circulo para filtrar o militar
    idmilitar = queryset[0].idmilitar
    idcirculo = queryset[0].idcirculo
    militar = get_object_or_404(Militar, id=idmilitar, idcirculo=idcirculo)

    template_name = 'editar_dispensa.html'
    context = {}
    #print(queryset)
    if request.method == 'POST':
        form = DispensaForm(request.POST, instance=queryset[0])
        if form.is_valid():
            form.save()
            return redirect('core:dispensar', idmilitar, idcirculo)
    else:
        form = DispensaForm(instance=queryset[0])

    disp_list = listar_dispensas(request, idmilitar, idcirculo, pagina)

    context = {'form': form,
                'militar': militar,
                'dispensado': disp_list
    }

    return render(request, template_name, context)

@login_required
def excluir_dispensa(request,iddispensa, pagina):
    queryset = Dispensas.objects.filter(id=iddispensa)
    #se não tiver dispensas retorna à tela principal das dispensas
    if (queryset.count()==0):
        return redirect('core:dispensar')

    #pega o id do militar e do circulo para filtrar o militar
    idmilitar = queryset[0].idmilitar
    idcirculo = queryset[0].idcirculo
    militar = get_object_or_404(Militar, id=idmilitar, idcirculo=idcirculo)
    template_name = 'excluir_dispensa.html'
    context = {}
    if request.method == 'POST':
        if (queryset.count()>0):
            queryset.delete()
        return redirect('core:dispensar', idmilitar, idcirculo)
    else:
        form = DispensaForm(instance=queryset[0])

    disp_list = listar_dispensas(request, idmilitar, idcirculo, pagina)

    context = {'form': form, 'militar': militar, 'dispensado': disp_list}

    return render(request, template_name, context)

#def contact(request):
#    return render(request, 'contact.html')