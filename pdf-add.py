import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def add_page_number(input_pdf, output_pdf):
    # Create a new PDF with page numbers
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Helvetica', 12)  # Setting font size to 12px
    pdf = PyPDF2.PdfReader(input_pdf)
    for page_num in range(len(pdf.pages)):
        page_width = letter[0]
        text_width = can.stringWidth(str(page_num + 1), 'Helvetica', 12)
        can.drawString(page_width - text_width - 30, 30, str(page_num + 1))  # 30px padding from bottom right
        can.showPage()
    can.save()
    packet.seek(0)
    new_pdf = PyPDF2.PdfReader(packet)
    pdf_writer = PyPDF2.PdfWriter()

    # Merge the two PDFs together
    for page_num in range(len(pdf.pages)):
        page = pdf.pages[page_num]
        page.merge_page(new_pdf.pages[page_num])
        pdf_writer.add_page(page)  # Corrected to use add_page

    with open(output_pdf, 'wb') as f:
        pdf_writer.write(f)

# Calling the function with 'pdf-input.pdf' as the source and 'output-with-numbers.pdf' as the output
add_page_number('pdf-input.pdf', 'output-with-numbers.pdf')
