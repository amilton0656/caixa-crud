from datetime import datetime
from io import BytesIO
import textwrap

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from apps.centros_custos.models import CentroCusto
from apps.obras.models import Obra

from .forms import MovimentoForm
from .models import Movimento


def login_view(request):
    if request.user.is_authenticated:
        return redirect('caixa:movimento_list')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect_to = request.GET.get('next')
            if redirect_to and url_has_allowed_host_and_scheme(redirect_to, allowed_hosts={request.get_host()}):
                return redirect(redirect_to)
            return redirect('caixa:movimento_list')
        messages.error(request, 'Usuario ou senha invalidos.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def movimento_list(request):
    movimentos = Movimento.objects.select_related('obra', 'centro_custos')

    obra_id = request.GET.get('obra', '').strip()
    centro_id = request.GET.get('centro_custos', '').strip()
    data_inicio = request.GET.get('data_inicio', '').strip()
    data_fim = request.GET.get('data_fim', '').strip()
    busca_historico = request.GET.get('historico', '').strip()

    if obra_id:
        movimentos = movimentos.filter(obra_id=obra_id)
    if centro_id:
        movimentos = movimentos.filter(centro_custos_id=centro_id)
    if data_inicio:
        try:
            inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            movimentos = movimentos.filter(data__gte=inicio)
        except ValueError:
            messages.warning(request, 'Data inicial invalida.')
    if data_fim:
        try:
            fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            movimentos = movimentos.filter(data__lte=fim)
        except ValueError:
            messages.warning(request, 'Data final invalida.')
    if busca_historico:
        movimentos = movimentos.filter(historico__icontains=busca_historico)

    paginator = Paginator(movimentos, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    context = {
        'movimentos': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'is_paginated': page_obj.has_other_pages(),
        'obras': Obra.objects.all(),
        'centros': CentroCusto.objects.all(),
        'filters': {
            'obra': obra_id,
            'centro_custos': centro_id,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'historico': busca_historico,
        },
        'show_filters': any([obra_id, centro_id, data_inicio, data_fim, busca_historico]),
        'querystring': query_params.urlencode(),
    }
    return render(request, 'caixa/list.html', context)


@login_required
def movimento_create(request):
    if request.method == 'POST':
        form = MovimentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('caixa:movimento_list')
    else:
        form = MovimentoForm()
    return render(request, 'caixa/form.html', {'form': form, 'title': 'Novo Movimento'})


@login_required
def movimento_update(request, pk: int):
    movimento = get_object_or_404(Movimento, pk=pk)
    if request.method == 'POST':
        form = MovimentoForm(request.POST, instance=movimento)
        if form.is_valid():
            form.save()
            return redirect('caixa:movimento_list')
    else:
        form = MovimentoForm(instance=movimento)
    return render(request, 'caixa/form.html', {'form': form, 'title': 'Editar Movimento'})


@login_required
def movimento_delete(request, pk: int):
    movimento = get_object_or_404(Movimento, pk=pk)
    if request.method == 'POST':
        movimento.delete()
        return redirect('caixa:movimento_list')
    return render(request, 'caixa/confirm_delete.html', {'movimento': movimento})


@login_required
def movimento_export_pdf(request):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y_position = height - 50

    pdf.setFont('Helvetica-Bold', 16)
    pdf.drawString(40, y_position, 'Relatorio de Movimentos')
    y_position -= 30
    pdf.setFont('Helvetica', 11)

    movimentos = Movimento.objects.select_related('obra', 'centro_custos')
    for movimento in movimentos:
        line = (
            f"ID: {movimento.id} | Obra: {movimento.obra.nome} | Centro: {movimento.centro_custos.descricao} | "
            f"Data: {movimento.data:%d/%m/%Y} | Sinal: {movimento.get_sinal_display()} | Valor: {movimento.valor:.2f} | Historico: {movimento.historico}"
        )
        for wrapped_line in textwrap.wrap(line, width=100):
            pdf.drawString(40, y_position, wrapped_line)
            y_position -= 16
            if y_position < 50:
                pdf.showPage()
                pdf.setFont('Helvetica', 11)
                y_position = height - 50
        y_position -= 8
        if y_position < 50:
            pdf.showPage()
            pdf.setFont('Helvetica', 11)
            y_position = height - 50

    pdf.save()
    buffer.seek(0)

    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=movimentos.pdf'
    return response


@login_required
def movimento_export_excel(request):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = 'Movimentos'

    worksheet.append(['ID', 'Obra', 'Centro de Custo', 'Data', 'Sinal', 'Valor', 'Historico'])
    movimentos = Movimento.objects.select_related('obra', 'centro_custos')
    for movimento in movimentos:
        worksheet.append([
            movimento.id,
            movimento.obra.nome,
            movimento.centro_custos.descricao,
            movimento.data.strftime('%d/%m/%Y'),
            movimento.get_sinal_display(),
            movimento.valor,
            movimento.historico,
        ])

    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=movimentos.xlsx'
    return response

from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas

def entregar_pdf(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "Olá, PDF gerado com ReportLab!")
    p.showPage()
    p.save()
    buffer.seek(0)
    resp = FileResponse(buffer, content_type="application/pdf")
    resp["Content-Disposition"] = 'attachment; filename="hello.pdf"'
    return resp

