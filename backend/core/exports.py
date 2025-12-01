from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(content):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.drawString(50, 800, "Rewritten Content:")
    pdf.drawString(50, 780, content[:500])  # simple display
    pdf.save()
    buffer.seek(0)
    return buffer
