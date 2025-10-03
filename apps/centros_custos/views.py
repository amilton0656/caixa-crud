from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .forms import CentroCustoForm
from .models import CentroCusto


@login_required
def centrocusto_list(request):
    centros = CentroCusto.objects.all()
    return render(request, 'centros_custos/list.html', {'centros': centros})


@login_required
def centrocusto_create(request):
    if request.method == 'POST':
        form = CentroCustoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('centros_custos:list')
    else:
        form = CentroCustoForm()
    return render(request, 'centros_custos/form.html', {'form': form, 'title': 'Novo Centro de Custo'})


@login_required
def centrocusto_update(request, pk: int):
    centro = get_object_or_404(CentroCusto, pk=pk)
    if request.method == 'POST':
        form = CentroCustoForm(request.POST, instance=centro)
        if form.is_valid():
            form.save()
            return redirect('centros_custos:list')
    else:
        form = CentroCustoForm(instance=centro)
    return render(request, 'centros_custos/form.html', {'form': form, 'title': 'Editar Centro de Custo'})


@login_required
def centrocusto_delete(request, pk: int):
    centro = get_object_or_404(CentroCusto, pk=pk)
    if request.method == 'POST':
        centro.delete()
        return redirect('centros_custos:list')
    return render(request, 'centros_custos/confirm_delete.html', {'centro': centro})


@login_required
def centrocusto_export_pdf(request):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y_position = height - 50

    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(40, y_position, 'Relatorio de Centros de Custo')
    y_position -= 30
    pdf.setFont('Helvetica', 11)

    for centro in CentroCusto.objects.all():
        line = f"{centro.id} - {centro.descricao}"
        pdf.drawString(40, y_position, line)
        y_position -= 18
        if y_position < 50:
            pdf.showPage()
            pdf.setFont('Helvetica', 11)
            y_position = height - 50

    pdf.save()
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=centros_de_custo.pdf'
    return response


@login_required
def centrocusto_export_excel(request):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Centros de Custo'

    worksheet.append(['ID', 'Descricao'])
    for centro in CentroCusto.objects.all():
        worksheet.append([centro.id, centro.descricao])

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=centros_de_custo.xlsx'
    return response
