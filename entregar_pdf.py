# views.py
from io import BytesIO
from django.http import FileResponse
from reportlab.pdfgen import canvas

def pdf_hello(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 750, "Olá, PDF gerado com ReportLab!")
    p.showPage()
    p.save()
    buffer.seek(0)
    resp = FileResponse(buffer, content_type="application/pdf")
    resp["Content-Disposition"] = 'attachment; filename="hello.pdf"'
    return resp
