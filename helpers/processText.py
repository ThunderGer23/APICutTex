from difflib import get_close_matches as gcm
from config.db import conn
from os import listdir as ld
from os import path as pth
from os import remove as rm
import requests
import PyPDF2
import re
# pdfRead = PyPDF2.PdfFileReader(open('document\TesisNotGenitoIndice.pdf', 'rb'))
Lon = 0
def processText(hojas, name, lon):
    global Lon
    Lon = lon
    p = list(map(lambda i : i.strip(), [''.join(list(filter(lambda i : (i.isalnum() or i==' '),p))) for p in list(hojas.lower().split('\n'))]))
    test = {'page':p[0]}
    for pa in range(len(p)): test[f's{pa}'] = p[pa]
    if (gcm(test['s1']) for x in ['indice','contenido']): test.pop('s1')
    test.pop('s0')
    coincidencias = list(set([ match for valor in test.values() for match in gcm((lambda x: x.split()[0] if len(x.split()) > 0 else "")(valor), ['objetivo', 'objetivos', 'marco', 'estado', 'planteamiento', 'justificación', 'análisis', 'funcional'],n = 10, cutoff=0.3) ]))
    resultados = [f"{k} {v}" for k, v in test.items() if any(c in v for c in coincidencias)]
    if(len(resultados)): sections(resultados, name)
    return test

def delnum(s):
    for i in range(10):
        s = s.replace(str(i),'')
    return s

def sections(section, name):
    pdfRead = PyPDF2.PdfFileReader(open(f'./document/{name}', 'rb'))
    s = {}
    ids = []
    match = ""
    secforana = ""
    for i in section:
        aux = i.split()
        s[aux[0]] = {"sec": " ".join(aux[1:-1]), "pag": aux[-1]}
    arr = list(s.keys())
    for i in range(len(arr)):
        title = " ".join(delnum(s[arr[i]]['sec']).split()[:-1])
        pretitle = " ".join(delnum(s[arr[i-1]]['sec']).split()[:-1])
        page = int(s[arr[i]]['pag'])
        pageRange = page - int(s[arr[i-1]]['pag'])
        regex = re.compile(pretitle + r' \n*(.*?).\n*'+ title, re.DOTALL)
        if (pageRange != 0):
            for ran in range(page - pageRange, page+1): secforana += pdfRead.getPage(ran-1).extract_text().lower()
            match = regex.search(secforana)
        else: match = regex.search(pdfRead.getPage(int(s[arr[i]]['pag'])-1).extract_text().lower())
        analysis = match.group(1) if(match != None) else None
        ids.append(str(conn.local.files.insert_one({"name": name,"data": analysis}).inserted_id))
        value = {"id": ids}
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        # response = requests.post('http://www.apipara-production.up.railway.app/document', headers=headers, json=value)
        # if(r.status_code): r.json()
        print(analysis)
        lista = ld('./document')
        for file_name in lista:
            [rm(pth.join("document", file)) for file in ld("document")]
        Lon -=1
    return analysis

