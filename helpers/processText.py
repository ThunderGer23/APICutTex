def processText(page, test: str):
    p = list(map(lambda i : i.strip(), [''.join(list(filter(lambda i : (i.isalnum() or i==' '),p))) for p in list(page.lower().split('\n'))]))
    p.pop([x for x in range(len(p)) if test in p[x]].pop())
    test = {'page':p[0]}
    for pa in range(len(p)): test[f's{pa}'] = p[pa]
    test.pop('s0')
    return test