from difflib import get_close_matches as gcm

def processText(hojas):
    p = list(map(lambda i : i.strip(), [''.join(list(filter(lambda i : (i.isalnum() or i==' '),p))) for p in list(hojas.lower().split('\n'))]))
    test = {'page':p[0]}
    for pa in range(len(p)): test[f's{pa}'] = p[pa]
    if (gcm(test['s1']) for x in ['indice','contenido']): test.pop('s1')
    test.pop('s0')

    coincidencias = list(set(
        [
            match
            for valor in test.values()
            for match in gcm((lambda x: x.split()[0] if len(x.split()) > 0 else "")(valor), ['objetivo', 'Objetivos', 'marco', 'estado', 'planteamiento', 'justificación', 'análisis', '5 CONCLUSIONES'],n = 10, cutoff=0.3)
        ]
    ))
    resultados = [f"{k} {v}" for k, v in test.items() if any(c in v for c in coincidencias)]
    if(len(resultados)): print(resultados)
    return test