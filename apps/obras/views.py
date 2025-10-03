from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .forms import ObraForm
from .models import Obra


@login_required
def obra_list(request):
    obras = Obra.objects.all()

    busca = request.GET.get('busca', '').strip()
    if busca:
        obras = obras.filter(nome__icontains=busca)

    paginator = Paginator(obras, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    context = {
        'obras': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'filters': {'busca': busca},
        'show_filters': bool(busca),
        'querystring': query_params.urlencode(),
    }
    return render(request, 'obras/list.html', context)


@login_required
def obra_create(request):
    if request.method == 'POST':
        form = ObraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('obras:list')
    else:
        form = ObraForm()
    return render(request, 'obras/form.html', {'form': form, 'title': 'Nova Obra'})


@login_required
def obra_update(request, pk: int):
    obra = get_object_or_404(Obra, pk=pk)
    if request.method == 'POST':
        form = ObraForm(request.POST, instance=obra)
        if form.is_valid():
            form.save()
            return redirect('obras:list')
    else:
        form = ObraForm(instance=obra)
    return render(request, 'obras/form.html', {'form': form, 'title': 'Editar Obra'})


@login_required
def obra_delete(request, pk: int):
    obra = get_object_or_404(Obra, pk=pk)
    if request.method == 'POST':
        obra.delete()
        return redirect('obras:list')
    return render(request, 'obras/confirm_delete.html', {'obra': obra})


@login_required
def obra_export_pdf(request):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y_position = height - 50

    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(40, y_position, 'Relatorio de Obras')
    y_position -= 30
    pdf.setFont('Helvetica', 11)

    for obra in Obra.objects.all():
        line = f"{obra.id} - {obra.nome} - {obra.endereco} - {obra.municipio}"
        pdf.drawString(40, y_position, line)
        y_position -= 18
        if y_position < 50:
            pdf.showPage()
            pdf.setFont('Helvetica', 11)
            y_position = height - 50

    pdf.save()
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=obras.pdf'
    return response


@login_required
def obra_export_excel(request):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Obras'

    worksheet.append(['ID', 'Nome', 'Endereco', 'Municipio'])
    for obra in Obra.objects.all():
        worksheet.append([obra.id, obra.nome, obra.endereco, obra.municipio])

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=obras.xlsx'
    return response
