from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import PyPDF2
import PyPDF2 as pypdf

######SIRVE PARA AGREGAR LA FRASE AL FINAL DE LAS HORAS ADEMÁS DE PODER INCLUIR QR O ALGO ASÍ

if __name__=='__main__':

    nombre_pdf_original = "doc_original.pdf" # Cambia aquí el nombre de tu documento original
    nombre_pdf_salida = "doc_estampado.pdf" # Cambia aquí el nombre del PDF de salida


    ####################MENSAJE BLANCO PARA TOAS LAS PAGINAS (EXCEPTO LA ÚLTIMA)####################################

    mensaje_blanco = ""
    packet_blanco = io.BytesIO()

    mi_canvas = canvas.Canvas(packet_blanco, pagesize=letter)
    mi_canvas.drawString(130, 40, mensaje_blanco)
    mi_canvas.save()

    packet_blanco.seek(0)

    pdf_con_pie_blanco = PdfFileReader(packet_blanco)

    ###########################################################

    mensaje = "Este documento ha sido firmado electrónicamente de acuerdo con la ley N° 19.799"
    packet = io.BytesIO()

    mi_canvas = canvas.Canvas(packet, pagesize=letter)
    mi_canvas.setFont('Times-Roman', 12)
    mi_canvas.drawString(130, 40, mensaje)
    mi_canvas.drawImage("qr.jpg", 85, 20, width=40, height=40)
    mi_canvas.save()

    packet.seek(0)

    pdf_con_pie = PdfFileReader(packet)



    pdf_existente = PdfFileReader(open(nombre_pdf_original, "rb"))
    output = PdfFileWriter()

    # Iterar desde 0 hasta el número de páginas de nuestro documento
    numero_de_paginas = pdf_existente.getNumPages()
    for numero in range(0, numero_de_paginas):

        if numero != numero_de_paginas - 1:
            page = pdf_existente.getPage(numero)
            page.mergePage(pdf_con_pie_blanco.getPage(0))
            output.addPage(page)

        else:
            page = pdf_existente.getPage(numero)
            page.mergePage(pdf_con_pie.getPage(0))
            output.addPage(page)




    outputStream = open(nombre_pdf_salida, "wb")
    output.write(outputStream)
    outputStream.close()



