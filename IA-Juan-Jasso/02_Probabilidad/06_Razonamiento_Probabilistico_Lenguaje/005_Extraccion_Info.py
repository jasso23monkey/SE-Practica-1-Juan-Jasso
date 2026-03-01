import collections

# Base de conocimiento (Lexicon) para clasificar entidades
DICCIONARIO_ENTIDADES = {
    # Personas (PER)
    "tim cook": "PER",
    "elon musk": "PER",
    "jeff bezos": "PER",
    
    # Organizaciones (ORG)
    "apple": "ORG",
    "tesla": "ORG",
    "spacex": "ORG",
    "amazon": "ORG",
    
    # Lugares (LOC)
    "cupertino": "LOC",
    "california": "LOC",
    "seattle": "LOC"
}

# La función tokenizar_entidades busca coincidencias exactas
def tokenizar_oracion(oracion):
    """
    Simula la tokenización avanzada (bigramas/trigramas)
    para capturar nombres compuestos.
    """
    return oracion.lower().split()

def extraer_entidades(oracion, diccionario):
    """
    Identifica entidades nombradas en una oración usando un enfoque
    simple basado en la coincidencia de bigramas y unigramas.
    """
    tokens = tokenizar_oracion(oracion)
    entidades_extraidas = []
    
    # 1. Buscar Trigramas y Bigramas (Ej: "Jeff Bezos" o "Tim Cook")
    i = 0
    while i < len(tokens):
        # Intenta un trigrama (Ej: 'Jeff Bezos' + algo más)
        if i + 2 < len(tokens):
            trigrama = " ".join(tokens[i:i+3])
            if trigrama in diccionario:
                entidades_extraidas.append((trigrama, diccionario[trigrama]))
                i += 3
                continue

        # Intenta un bigrama (Ej: 'Tim Cook')
        if i + 1 < len(tokens):
            bigrama = " ".join(tokens[i:i+2])
            if bigrama in diccionario:
                entidades_extraidas.append((bigrama, diccionario[bigrama]))
                i += 2
                continue
        
        # 2. Buscar Unigramas (Ej: 'Apple')
        unigrama = tokens[i]
        if unigrama in diccionario:
            entidades_extraidas.append((unigrama, diccionario[unigrama]))
        
        i += 1
        
    return entidades_extraidas

# --- 3. Ejecución del Proceso de IE ---

TEXTO_NO_ESTRUCTURADO = "Tim Cook, el CEO de Apple, visitó la sede de Amazon en Seattle."

entidades_encontradas = extraer_entidades(TEXTO_NO_ESTRUCTURADO, DICCIONARIO_ENTIDADES)

print("=====================================================")
print("      EXTRACCIÓN DE INFORMACIÓN (NER) SIMPLE         ")
print("=====================================================")
print(f"Texto de Entrada: {TEXTO_NO_ESTRUCTURADO}")
print("-" * 50)
print("RESULTADO ESTRUCTURADO (Entidades Extraídas):")

for entidad, tipo in entidades_encontradas:
    print(f"  - Entidad: '{entidad.title()}' | Tipo: {tipo}")