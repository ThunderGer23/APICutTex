import PyPDF2
from fastapi import APIRouter
from difflib import get_close_matches as gcm
from itertools import chain
from helpers.processText import processText as pT
FI = chain.from_iterable
indice = {}

cF = APIRouter()

# 'document\TesisNotGenitoIndice.pdf'
@cF.get('/indice', response_model= dict, tags=['Get indice'])
def readFile(rute: str):
    pdfRead = PyPDF2.PdfFileReader(open(rute, 'rb'))
    for i in range(0, int(pdfRead.getNumPages()/10)):
        page = pdfRead.getPage(i)
        test = list(FI([gcm(x,page.extract_text().lower()[:20].split(' ')) for x in ['indice','contenido']]))
        if (len(test) and ((test[0] == 'índice') or (test[0] == 'contenido'))): indice['Ip'+str(i)] = pT(page.extract_text(), test[0])
    # Aquí se mandan las peticiones a la API de parafraseo, en base al contenido del indice
    return indice