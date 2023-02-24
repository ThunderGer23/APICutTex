import PyPDF2
from difflib import get_close_matches as gcm
from itertools import chain
fi = chain.from_iterable

pdfFile = open('document\TesisNotGenitoIndice.pdf', 'rb')
pdfRead = PyPDF2.PdfFileReader(pdfFile)
indice = {}

def keepalnum(i):
    return (i.isalnum() or i==' ')

def processText(page: str, test: str):
    page = [''.join(list(filter(keepalnum,p))) for p in list(page.lower().split('\n'))]
    # page = page.replace('.', ' ').lower().split('\n')
    page = [p.strip() for p in page]
    title = page.index(gcm(test, page)[0])
    page.pop(title)
    page = [list(filter(('').__ne__,p.split(' '))) for p in page]
    # Test = list(filter(keepalnum,page))
    test = {'page':page[0]}
    for p in range(len(page)):
        test[f's{p}'] = page[p]
    test.pop('s0')
    return test
    
        

def readFile():
    for i in range(0, pdfRead.getNumPages()):
        page = pdfRead.getPage(i)
        # print('Page: '+str(i))
        compare = page.extract_text().lower()[:20].split(' ')
        test = list(fi([gcm(x,compare) for x in ['indice','contenido']]))
        if(len(test)):
            global indice
            indice = processText(page.extract_text(), test[0])
            pass
        if (gcm(x,indice.get('page')) for x in [page.extract_text()]):
            pass
        else:
            print(page.extract_text())
            print('holi') 
        #Jalar texto :'v

readFile()