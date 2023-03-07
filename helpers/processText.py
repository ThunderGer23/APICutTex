from difflib import get_close_matches as gcm
import PyPDF2
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

def sections(section):
    # print(section)
    # print(list(i.split() for i in section))
    pdfRead = PyPDF2.PdfFileReader(open('document\TesisNotGenitoIndice.pdf', 'rb'))
    s = {}
    for i in section:
        aux = i.split()
        s[aux[0]] = {
            "sec": aux[1:-1],
            "pag": aux[-1]}

