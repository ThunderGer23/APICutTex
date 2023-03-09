from difflib import get_close_matches as gcm
import PyPDF2
import re
pdfRead = PyPDF2.PdfFileReader(open('document\TesisNotGenitoIndice.pdf', 'rb'))

def processText(hojas):
    p = list(map(lambda i : i.strip(), [''.join(list(filter(lambda i : (i.isalnum() or i==' '),p))) for p in list(hojas.lower().split('\n'))]))
    test = {'page':p[0]}
    for pa in range(len(p)): test[f's{pa}'] = p[pa]
    if (gcm(test['s1']) for x in ['indice','contenido']): test.pop('s1')
    test.pop('s0')

    coincidencias = list(set([ match for valor in test.values() for match in gcm((lambda x: x.split()[0] if len(x.split()) > 0 else "")(valor), ['objetivo', 'objetivos', 'marco', 'estado', 'planteamiento', 'justificación', 'análisis', 'funcional'],n = 10, cutoff=0.3) ]))
    
    resultados = [f"{k} {v}" for k, v in test.items() if any(c in v for c in coincidencias)]
    if(len(resultados)): sections(resultados)
    return test

def delnum(s):
    for i in range(10):
        s = s.replace(str(i),'')
    return s

def sections(section):
    # print(list(i.split() for i in section))
    s = {}
    secforana = ""
    CONT = 0
    for i in section:
        aux = i.split()
        s[aux[0]] = {"sec": " ".join(aux[1:-1]), "pag": aux[-1]}

    arr = list(s.keys())
    for i in range(2, len(arr)):
        title = " ".join(delnum(s[arr[i]]['sec']).split()[:-1])
        pretitle = " ".join(delnum(s[arr[i-1]]['sec']).split()[:-1])
        page = int(s[arr[i]]['pag'])
        pageRange = page - int(s[arr[i-1]]['pag'])
        regex = re.compile(pretitle + r' \n*(.*?).\n*'+ title, re.DOTALL)

        if (pageRange != 0):
            print(title)
            print(pretitle)
            # caso especialpara que las secciones de 2 hojas las imprima
            for ran in range(page, page + pageRange):
                pa = pdfRead.getPage(ran-1).extract_text().lower()
                secforana += pa
            match = regex.search(secforana)
            if(match != None):
                sec = match.group(1)
                print(sec)
                CONT += 1
        else:
            # print(pageRange)
            # print(title)
            # print(pretitle)
            pa = pdfRead.getPage(int(s[arr[i]]['pag'])-1).extract_text().lower()
            match = regex.search(pa)
            if(match != None):
                sec = match.group(1)
                print(sec)
                CONT += 1
        # if(CONT == 5): break
        # print(pretitle, title)
        # # No encuentra porque hay que guardar el rando de hojas en donde se va a buscar
        # # Si ambos están en la misma hoja solo lee una y ya, si son diferentes hace un
        # # append a un array de las hojas y extrae el texto de todas ellas para después seccionar
        # page = pdfRead.getPage(int(s[arr[i]]['pag'])-1).extract_text().lower()
        # regex = re.compile(pretitle+r' \n*(.*?).\n*'+title, re.DOTALL)
        # match = regex.search(page)
        # if(match != None):
        #     sec = match.group(1)
            # print(sec)
        # break
    # return s

