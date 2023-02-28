import PyPDF2
from difflib import get_close_matches as gcm
from itertools import chain
fi = chain.from_iterable

pdfFile = open('document\TesisNotGenitoIndice.pdf', 'rb')
pdfRead = PyPDF2.PdfFileReader(pdfFile)
indice = {}

def processText(page, test: str):
    page = [''.join(list(filter(lambda i : (i.isalnum() or i==' '),p))) for p in list(page.lower().split('\n'))]
    page = list(map(lambda i : i.strip(), page))
    page.pop([x for x in range(len(page)) if test in page[x]].pop())
    test = {'page':page[0]}
    for p in range(len(page)):
        test[f's{p}'] = page[p]
    test.pop('s0')
    return test

def readFile():
    for i in range(0, int(pdfRead.getNumPages()/10)):
        page = pdfRead.getPage(i)
        # print('Page: '+str(i))
        compare = page.extract_text().lower()[:20].split(' ')
        test = list(fi([gcm(x,compare) for x in ['indice','contenido']]))
        if(len(test) and ((test[0] == 'índice') or (test[0] == 'contenido'))):
            print("this is a test: ",test)
            global indice
            indice = processText(page.extract_text(), test[0])
            print(indice)
            pass
        if (gcm(x,indice.get('page')) for x in [page.extract_text()]):
            pass
readFile()