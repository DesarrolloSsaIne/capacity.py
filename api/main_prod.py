import requests
import json
import base64, os
import jwt
import hashlib
import math
import sys
import time
from base64 import b64decode
import imgkit
from datetime import datetime, timedelta


if __name__=='__main__':

    a= 0


    #####//Código en caso que se requiera información adicional dinámica en la imagen de lo contrario no es necesario####
    path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
    config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)
    # imgkit.from_file('mihtml.html', 'table.jpg',config=config)

    html_str='<img src="1.png" width="150" height="150"><div>INE</div>'
    Html_file = open("mihtml.html", "w")
    Html_file.write(html_str)
    Html_file.close()
    options = {

        'crop-h': '400',
        'crop-w': '170',
        'quiet': '',

    }

    imgkit.from_file('mihtml.html', 'out2.png', config=config, options=options)
    #####//Código en caso que se requiera información adicional dinámica en la imagen de lo contrario no es necesario####




    # ##Convierte a Base64 el documento pdf hasta 20 megas
    with open('out2.png', 'rb') as timbre_file:
        jpg_file64 = base64.b64encode(timbre_file.read()).decode('utf-8')

    url = 'https://api.firma.digital.gob.cl/firma/v2/files/tickets'

    now = datetime.now() + timedelta(seconds=300) # Fecha expiración del token + 300 segundos
    exp_plus = now.strftime("%Y-%m-%dT%H:%M:%S")

    exp=exp_plus

    otp='759228'

    layout='<AgileSignerConfig><Application id=\"THIS-CONFIG\"><pdfPassword/><Signature><Visible active=\"true\" layer2=\"true\" label=\"true\" pos=\"1\"><llx>30</llx><lly>110</lly><urx>400</urx><ury>220</ury><page>LAST</page><image>BASE64</image><BASE64VALUE>'+str(jpg_file64)+'</BASE64VALUE></Visible></Signature></Application></AgileSignerConfig>'


    tokenDesatendido = jwt.encode({'entity': 'Instituto Nacional de Estadísticas',
                        'run':'10685080',
                        'expiration': exp,
                        'purpose':'Desatendido'},
                        'a08253d568bf46f2a5ef8217dbb06da7', algorithm='HS256').decode('utf-8')

    tokenAtendido = jwt.encode({'entity': 'Instituto Nacional de Estadísticas',
                        'run':'14202112',
                        'expiration': exp,
                        'purpose':'Propósito General'},
                        'a08253d568bf46f2a5ef8217dbb06da7', algorithm='HS256').decode('utf-8')



    with open('doc.pdf', 'rb') as pdf_file: # Convierte a Base64 el documento pdf hasta 20 megas
        pdfb64 = base64.b64encode(pdf_file.read()).decode('utf-8')


    with open('doc.pdf', "rb") as f: # Genera el checksum desde el documento pdf hasta 20 megas
        bytesConv = f.read()
        readable_hash = hashlib.sha256(bytesConv).hexdigest()
        checksum= readable_hash


    files ={'api_token_key':'99c3f6e0-24c9-4c58-a564-dfde158cb987',
            'token':tokenDesatendido, 'files': [{'content-type': 'application/pdf',
             'content': pdfb64, 'description':'Str', 'layout':layout,
             'checksum': checksum}]}


    headers = {'content-type': 'application/json'} # 'OTP':otp     (agregar cuando es atendido)

    response = requests.post(url, data=json.dumps(files), headers=headers)


    if response.status_code==200:

        print(response.status_code)

        response_str=response.text #Estrae la respuesta como str
        response_dic = json.loads(response_str) # la convierte en una estructura json

        files_dic= response_dic['files'][0] #Estrae files
        pdfb64Signed = files_dic['content'] #estraes el content (base64 del archivo firmado)

        pdfSigned = base64.b64decode(str(pdfb64Signed)) # convierte a pdf

        with open(os.path.expanduser('DocumentoFirmadoProd.pdf'), 'wb') as fout: #guarda el pdf en carpeta
            fout.write(pdfSigned)
            fout.close()

    else:
        # print(archivo)
        print(response.status_code)
        print(response.content)








        ############### CONVERTIR HTML A IMAGEN CON UNA API ####################

    # HCTI_API_ENDPOINT = "https://hcti.io/v1/image"
    # HCTI_API_USER_ID = '41ddfc76-5cbe-4bca-b632-f0c8f9fccce7'
    # HCTI_API_KEY = '0d9fcbba-fdb0-4770-9fad-7545dc4f089b'
    #
    # data = {'html': "<div class='box'>Timbre Firma"+ str(a)+"</div>",
    #         'css': ".box { color: white; background-image: url('1.png'); background-color: #0f79b9; padding: 10px; font-family: Roboto }",
    #         'google_fonts': "Roboto"}
    #
    # image = requests.post(url=HCTI_API_ENDPOINT, data=data, auth=(HCTI_API_USER_ID, HCTI_API_KEY))
    #
    # url_imagen = image.json()['url']  # El link de la imagen
    # nombre_local_imagen = "go3.jpg"  # El nombre con el que queremos guardarla
    # imagen = requests.get(url_imagen).content
    # with open(nombre_local_imagen, 'wb') as handler:
    #     handler.write(imagen)

        ############### CONVERTIR HTML A IMAGEN CON UNA API ####################