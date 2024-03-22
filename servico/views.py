from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# from .forms import *
from .models import Servicos
from pessoal.models import Militar


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
    # para gerar pdf
    import io
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.units import inch
    from reportlab.lib.colors import black, red, olive
    from django.http import FileResponse

    from previsao.views import vermelha #, getPostoGraduacao

    sqlmilitar = "SELECT a.id, a.posto, a.codom,a.antiguidade,b.nomeguerra,\
    b.folga,b.data,b.dia, b.folga,c.descricao FROM pessoal_militar a, \
    servico_servicos b, core_escala c WHERE a.id=b.idmilitar AND \
    c.id=b.idescala AND a.idcirculo=b.idcirculo \
    ORDER BY b.data, c.precedencia, b.idcirculo, a.antiguidade"

    servico_list = Militar.objects.raw(sqlmilitar)
    data = servico_list[0].data
    dia = servico_list[0].dia
    fontColor = "black"
    if vermelha(data):
        fontColor = "red"

    titulo = 'PREVISÃO DE ESCALA DE SERVIÇO'
    # subtitulo = ' PARA O MÊS DE ' +nome_mes +' '+ str(data.year)

    p.setTitle(titulo)
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(black)
    p.drawCentredString(300, 795, titulo)
    # p.drawCentredString(300, 780, subtitulo)
    p.line(30,775,555,775)
    p.setFillColor(olive, alpha=0.75 )
    p.rect(30,755,525,20, fill=True, stroke=False)    
    

    p.setFillColor(white)
    p.setFont("Helvetica-Bold", 11)
    coluna1 = 'Data  - dia da Semana'
    coluna2 = 'Escala'
    coluna3 = 'Posto/Grad'
    coluna4 = 'Militar'
    coluna5 = 'OM'
    p.drawCentredString(105,760,  coluna1.upper())
    p.drawString(190,760, coluna2.upper())
    p.drawString(270,760, coluna3.upper())
    p.drawString(360,760, coluna4.upper())
    p.drawString(470,760, coluna5.upper())

    subtitle = data.strftime("%d/%m/%Y") + ' - ' + dia
    p.setFont("Helvetica", 11)
    p.setFillColor(fontColor)
    p.drawString(35, 735, subtitle)

    #---------------------- linhas verticais ----------------------
    p.line(180,775,180,755)
    p.line(260,775,260,755)
    p.line(350,775,350,755)
    p.line(460,775,460,755)
    #--------------------------------------------------------------

    p.line(30,755,555,755)
    p.setFont("Helvetica", 11)          
    # p.drawString(45,760, 'Data  - Dia da Semana      Escala             Posto>
    y = 755
    for escalado in servico_list:
        if (escalado.data != data):
            y -= 10
            data = escalado.data
            dia = escalado.dia
            fontColor = "black"

            p.line(30,y,555,y)

            if vermelha(data):
                fontColor = "red"

            # subtitle = 'Para o dia: ' + data.strftime("%d/%m/%Y") + ' - ' + d>
            if (y > 60):
                subtitle = data.strftime("%d/%m/%Y") + ' - ' + dia
                p.setFont("Helvetica", 11)
                p.setFillColor(fontColor)
                p.drawString(35, y-21, subtitle)
                p.setFont("Helvetica", 11)
                p.setFillColor(black)
                y -= 0
            elif (y > 40):
                p.drawString(35,y-12, 'Relatório gerado por: '+request.user.username + ' em: ' + datetime.now().strftime("%d/%m/%Y"))

        if y < 60:
            y = 755
            # adiciona uma nova página para continuar listando a escala
            p.showPage()
            p.setTitle(titulo)
            p.setFont("Helvetica-Bold", 14)
            p.setFillColor(black)
            p.drawCentredString(300, 795, titulo)
            # p.drawCentredString(300, 780, subtitulo)
            p.line(30,775,555,775)
            p.setFillColor(olive, alpha=0.75 )
            p.rect(30,755,525,20, fill=True, stroke=False)    
            

            p.setFillColor(white)
            p.setFont("Helvetica-Bold", 11)
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

            subtitle = data.strftime("%d/%m/%Y") + ' - ' + dia
            p.setFont("Helvetica", 11)
            p.setFillColor(fontColor)
            p.drawString(35, 735, subtitle)

            #---------------------- linhas verticais ----------------------
            p.line(180,775,180,755)
            p.line(260,775,260,755)
            p.line(350,775,350,755)
            p.line(460,775,460,755)
            #--------------------------------------------------------------

            p.line(30,755,555,755)
            p.setFont("Helvetica", 11)    
            p.setFillColor(black)
            # pdf.drawString(45,750, 'Escala             Posto/Grad          Mi>
        p.line(180,y+0,180,y-22)
        p.line(260,y+0,260,y-22)
        p.line(350,y+0,350,y-22)
        p.line(460,y+0,460,y-22)

        y -= 12
        # p.drawString(47, x, '{}: {} - {}'.
        #              format(escalado.descricao, getPostoGraduacao(escalado.po>
        p.drawString(185, y-2,escalado.descricao)
        p.drawString(265, y-2,escalado.get_posto_display())
        p.drawString(355, y-2,escalado.nomeguerra)
        p.drawString(465, y-2,escalado.get_codom_display())
 
    # # Create a file-like buffer to receive PDF data.
    # buffer = io.BytesIO()

    # # Create the PDF object, using the buffer as its "file."
    # p = canvas.Canvas(buffer)

    # # Draw things on the PDF. Here's where the PDF generation happens.
    # # See the ReportLab documentation for the full list of functionality.
    # # p.drawString(100, 100, "Hello world.")

    # p.setTitle('Serviços tirados')
    # p.setFont("Helvetica-Bold", 14)
    # p.drawString(245, 780, 'Serviços tirados')
    # subtitle = 'Para o dia: ' + data.strftime("%d/%m/%Y") + ' - ' + dia
    # p.setFont("Helvetica-Bold", 12)
    # p.setFillColor(fontColor)
    # p.drawString(45, 760, subtitle)
    # p.setFillColor(black)
    # p.setFont("Helvetica", 12)
    # # pdf.drawString(45,750, 'Escala             Posto/Grad          Militar')
    # x = 750
    # for escalado in servico_list:
    #     if (escalado.data != data):
    #         x -= 20
    #         data = escalado.data
    #         dia = escalado.dia
    #         fontColor = "black"
    #         if vermelha(data):
    #             fontColor = "red"

    #         subtitle = 'Para o dia: ' + data.strftime("%d/%m/%Y") + ' - ' + dia
    #         p.setFont("Helvetica-Bold", 12)
    #         p.setFillColor(fontColor)
    #         p.drawString(45, x, subtitle)
    #         p.setFont("Helvetica", 12)
    #         p.setFillColor(black)
    #         x -= 5

    #     if x < 40:
    #         x = 750
    #         # adiciona uma nova página para continuar listando a escala
    #         p.showPage()
    #         p.setFont("Helvetica-Bold", 14)
    #         p.drawString(245, 780, 'Serviços tirados')
    #         subtitle = 'Para o dia: ' + data.strftime("%d/%m/%Y") + ' - ' + dia
    #         p.setFont("Helvetica-Bold", 12)
    #         p.setFillColor(fontColor)
    #         p.drawString(45, 760, subtitle)
    #         p.setFont("Helvetica", 12)
    #         p.setFillColor(black)
    #         # pdf.drawString(45,750, 'Escala             Posto/Grad          Militar')

    #     x -= 15
    #     p.drawString(47, x, '{}: {} - {}'.
    #                  format(escalado.descricao, escalado.get_posto_display(), escalado.nomeguerra))

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='servicosTirados.pdf')