import PyPDF2
from fastapi import APIRouter
from difflib import get_close_matches as gcm
from itertools import chain
from helpers.processText import processText as pT
FI = chain.from_iterable
indice = {}
hojas = []
control = 0
cF = APIRouter()

# 'document\TesisNotGenitoIndice.pdf'
@cF.get('/indice', response_model= dict, tags=['Get indice'])
def readFile(rute: str):
    global control
    pdfRead = PyPDF2.PdfFileReader(open(rute, 'rb'))
    for i in range(0, int(pdfRead.getNumPages()/10)):
        if(len(list(FI([gcm(x,pdfRead.getPage(i).extract_text().lower()[:20].split(' ')) for x in ['indice','contenido']])))): hojas.append(i)

    for i in range(1, len(hojas)):
        for hoja in range(hojas[i-1], hojas[i]): indice['Ip'+str(hoja)] = pT(pdfRead.getPage(hoja).extract_text())
    indice['Ip'+str(hojas[-1])] = pT(pdfRead.getPage(hojas[-1]).extract_text())
    # Aquí se mandan las peticiones a la API de parafraseo, en base al contenido del indice
    # print(pdfRead.getPage(27).extract_text().lower()[:])
    return indice