import PyPDF2
from fastapi import APIRouter
from models.app import Files
from difflib import get_close_matches as gcm
from config.db import conn
from itertools import chain
from bson.objectid import ObjectId
from os import listdir
from os.path import exists
from helpers.processText import processText as pT
FI = chain.from_iterable
indice = {}
hojas = []
control = 0
cF = APIRouter()
from notigram import ping

# 'document\TesisNotGenitoIndice.pdf'
@cF.get('/document', response_model= dict, tags=['indice'])
def readFile(files):
    global control
    lon = len(files)
    for name in files:
        pdfRead = PyPDF2.PdfFileReader(open(f'./document/{name}', 'rb'))
        for i in range(0, int(pdfRead.getNumPages()/10)):
            if(len(list(FI([gcm(x,pdfRead.getPage(i).extract_text().lower()[:20].split(' ')) for x in ['indice','contenido']])))): hojas.append(i)

        for i in range(1, len(hojas)):
            for hoja in range(hojas[i-1], hojas[i]): indice['Ip'+str(hoja)] = pT(pdfRead.getPage(hoja).extract_text(), name, lon)
        indice['Ip'+str(hojas[-1])] = pT(pdfRead.getPage(hojas[-1]).extract_text(), name, lon)
    return indice

@cF.post('/document', tags=['indice'])
def createFile(files: Files):
    ping('daa39d53-6283-47a1-b945-b7ee6528dde0', 'Iniciando fileteo de documentos')
    filesave = []
    for id in files.id:
        file = conn.local.files.find_one({"_id": ObjectId(id)})
        file_name = file['name']
        filesave.append(file_name)
        with open(f'./document/{file_name}', 'wb') as f:
            f.write(file['data'])
    # print(files)
    readFile(filesave)
    return 'ok'
    