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
def gerarPDF(request, sql, titulo, subtitulo=None):
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import inch
    from reportlab.lib.colors import black, red, olive, white, blue
    from previsao.views import vermelha

    lista = Militar.objects.raw(sql)
    
    data = lista[0].data
    dia = lista[0].dia
    nome_mes = obterMes(data)
    dia = nomeDiaSemana(data)


    if (subtitulo != None):
        subtitulo += nome_mes + ' ' + str(data.year)

    fontColor = "black"
    if vermelha(data):
        fontColor = "red"

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    # ------------ Configura fonte, tamanho e cor da fonte ------------
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(black)
    # -----------------------------------------------------------------

    # ----------------- Escreve o Título do relatório -----------------
    p.setTitle(titulo)
    p.drawCentredString(300, 795, titulo)
    # -----------------------------------------------------------------

    # ---------------- Escreve o Subtítulo do relatório ---------------
    if (subtitulo !=None): 
        p.drawCentredString(300, 780, subtitulo)
    # -----------------------------------------------------------------

    # ----------------- Desenha o Cabeçalho da Tabela -----------------
    p.line(30,775,555,775)
    p.setFillColor(olive, alpha=0.75 )
    p.rect(30,755,525,20, fill=True, stroke=False)    
    p.line(30,755,555,755)
    # -----------------------------------------------------------------

    # ------------ Configura fonte, tamanho e cor da fonte ------------
    comumFontSize = 11
    p.setFillColor(white)
    p.setFont("Helvetica-Bold", comumFontSize)
    # -----------------------------------------------------------------

    # ----------- Configura os campos das colunas da tabela -----------
    coluna1 = 'Data  - dia da Semana'
    coluna2 = 'Escala'
    coluna3 = 'Posto/Grad'
    coluna4 = 'Militar'
    coluna5 = 'OM'
    # -----------------------------------------------------------------

    # ---------------- Escreve os títulos das colunas  ----------------
    #          upper é para deixar todas as letras maiúsculas         #
    # -----------------------------------------------------------------   
    p.drawCentredString(105,760,  coluna1.upper())
    p.drawString(190,760, coluna2.upper())
    p.drawString(270,760, coluna3.upper())
    p.drawString(360,760, coluna4.upper())
    p.drawString(470,760, coluna5.upper())
    # -----------------------------------------------------------------

    #---------------------- linhas verticais ----------------------
    p.line(180,775,180,755)
    p.line(260,775,260,755)
    p.line(350,775,350,755)
    p.line(460,775,460,755)
    #--------------------------------------------------------------

    topoPagina = 755
    rodapePagina = 40
    y = topoPagina
    areaUtil = topoPagina-rodapePagina
    nrlinhas = 0
    nrRegPorPag = 1
    deltaY = comumFontSize
    nrRegAtual = 0

    saltoTexto = 12
    saltoLinhas = 5


    # ------------ Configura fonte, tamanho e cor da fonte ------------
    p.setFillColor(fontColor)
    p.setFont("Helvetica", comumFontSize)   
    #------------------------------------------------------------------

    # - Faz uma varredura na lista para pegar todas escalas das datas -
    for escalado in lista:
        # --------- este if faz a mudança do dia da escala ------------
        if (escalado.data != data):
            nrRegAtual += 1
            # nrRegPorPag = (areaUtil // ((nrlinhas-1)*comumFontSize+(nrlinhas-1)*18))
            nrRegPorPag = (areaUtil // ((nrlinhas)*(saltoLinhas+saltoTexto)))
            print(nrRegPorPag)
            # print('atual e regporpaginas: ', nrRegAtual, nrRegPorPag)

            # -----------------------------------------------------------
            # O número 12 usado para calcular o deltaY é o equivalente ao 
            # salto de 12 pixels que é dado entre cada linha y -= saltoTexto
            # -----------------------------------------------------------
            deltaY = (saltoTexto*(nrlinhas-1)//2) 
            subtitle = data.strftime("%d/%m/%Y") + ' - ' + dia
            p.drawString(35, y+deltaY, subtitle)

            # y -= 10
            # y -= 6
            y -= saltoLinhas                     
            p.line(30,y,555,y)
            # p.line(30,y-saltoLinhas,555,y-saltoLinhas)

            #atualiza a data e o dia da semana para os valores do registro atual
            data = escalado.data
            dia = escalado.dia

            #configura a cor para preta, para garantir que não seja impresso de outra cor
            fontColor = "black"

            # if vermelha(data):
            #     fontColor = "red"

            if ((nrRegAtual < nrRegPorPag)):
                # print('Passou em regatual < regporpagina')
                if(vermelha(data)):
                    print('vermelha')
                    p.setFillColor(red, alpha=0.35 )
                    # print('O valor de y é: ',y)                        
                    deslocamento = (nrlinhas//2)+nrlinhas%2
                    if(nrlinhas % 2 != 0):
                        deslocamento = deltaY+deslocamento*saltoTexto+saltoLinhas
                    else:
                        deslocamento = deltaY+deslocamento*saltoTexto+2*saltoLinhas+1
                        
                    print("Deltay: ", deltaY, nrlinhas)
                    print('Deslocamento', deslocamento)
                    print('Y novo: ', y-deslocamento)
                    # p.rect(30,y-(deltaY+(nrlinhas//2)*saltoTexto+2*saltoLinhas+1),525,deltaY+(saltoTexto*(nrlinhas//2)+2*saltoLinhas), fill=True, stroke=False)
                    # p.rect(30,y-(deltaY+deslocamento*saltoTexto+saltoLinhas),525,deltaY+(saltoTexto*deslocamento+saltoLinhas), fill=True, stroke=False)
                    p.rect(30,y-deslocamento,525,deslocamento, fill=True, stroke=False)

                p.setFillColor(fontColor)
                # y -= 0
                nrlinhas = 0
                # print('Registro atual: ',nrRegAtual)   
                # print('Registros por página: ', nrRegPorPag)     

            if (nrRegAtual == nrRegPorPag):
                # print('passou aqui')
                p.setFillColor(fontColor)
                gerarRodape(request, p, y)
            
            # y -= 6                     
            # y -= saltoLinhas                     
        # if (y < 60):
        # força quebra de página, pq a quantidade de registros é igual ao que cabe em uma página
        if ((nrRegAtual == nrRegPorPag)):
            # print('deltay', deltaY, nrlinhas)
            nrRegAtual = 0
            nrlinhas = 0
            y = 755
    
            # adiciona uma nova página para continuar listando a escala
            p.showPage()
            p.setTitle(titulo)
            p.setFont("Helvetica-Bold", 14)
            p.setFillColor(black)
            p.drawCentredString(300, 795, titulo)
            if (subtitulo !=None):
                p.drawCentredString(300, 780, subtitulo)

            p.line(30,775,555,775)
            p.setFillColor(olive, alpha=0.75 )
            p.rect(30,755,525,20, fill=True, stroke=False)    
            

            p.setFillColor(white)
            p.setFont("Helvetica-Bold", comumFontSize)
            coluna1 = 'Data  - dia da Semana'
            coluna2 = 'Escala'
            coluna3 = 'Posto/Grad'
            coluna4 = 'Militar'
            coluna5 = 'OM'
            p.drawString(40,760,  coluna1.upper())
            p.drawString(190,760, coluna2.upper())
            p.drawString(270,760, coluna3.upper())
            p.drawString(360,760, coluna4.upper())
            p.drawString(470,760, coluna5.upper())

            #---------------------- linhas verticais ----------------------
            p.line(180,775,180,755)
            p.line(260,775,260,755)
            p.line(350,775,350,755)
            p.line(460,775,460,755)
            #--------------------------------------------------------------

            p.line(30,755,555,755)
            p.setFont("Helvetica", comumFontSize)    
            p.setFillColor(black)

        nrlinhas += 1

        p.line(180,y+0,180,y-(saltoLinhas+saltoTexto))
        p.line(260,y+0,260,y-(saltoLinhas+saltoTexto))
        p.line(350,y+0,350,y-(saltoLinhas+saltoTexto))
        p.line(460,y+0,460,y-(saltoLinhas+saltoTexto))

        # y -= 12
        y -= saltoTexto

        p.drawString(185, y-2,escalado.descricao)
        p.drawString(265, y-2,escalado.get_posto_display())
        p.drawString(355, y-2,escalado.nomeguerra)
        p.drawString(465, y-2,escalado.get_codom_display())
    # ----------------------- fim do for


    # Close the PDF object cleanly, and we're done.
    
    if (y > 60 & p.pageHasData()==False):
        ## - Coloca os dados última escala.
        subtitle = data.strftime("%d/%m/%Y") + ' - ' + dia
        p.drawString(35, y+deltaY, subtitle)

        # p.line(30,y-saltoLinhas,555,y- saltoLinhas)

        y -= saltoLinhas
        p.setFillColor(fontColor)
        gerarRodape(request, p, y)

    p.line(30,y,555,y)
    
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    return buffer



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