import PyPDF2
from difflib import get_close_matches as gcm
from itertools import chain
fi = chain.from_iterable

pdfFile = open('document\TesisNotGenitoIndice.pdf', 'rb')
pdfRead = PyPDF2.PdfFileReader(pdfFile)

def keepalnum(i):
    for j in i:
        if not (j.isalnum()):
            i.remove(j)
    return i

def processText(page: str, test: str):
    page = page.replace('.', ' ').lower().split('\n')
    page = [p.strip() for p in page]
    title = page.index(gcm(test, page)[0])
    page.pop(title)
    page = [list(filter(('').__ne__,p.split(' '))) for p in page]
    # Test = list(filter(keepalnum,page))
    # print(Test)
    Test = []
    for i in page:
        for j in i:
            if not(j.isalnum()):
                j = j[1:]
            Test.append(j)
    print(Test)
        

def readFile():
    for i in range(0, pdfRead.getNumPages()):
        page = pdfRead.getPage(i)
        # print('Page: '+str(i))
        compare = page.extract_text().lower()[:20].split(' ')
        test = list(fi([gcm(x,compare) for x in ['indice','contenido']]))
        if(len(test)):
            processText(page.extract_text(), test[0])
            break

readFile()