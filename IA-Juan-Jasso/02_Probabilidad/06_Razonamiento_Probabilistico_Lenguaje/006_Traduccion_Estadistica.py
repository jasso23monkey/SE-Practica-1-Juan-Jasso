import numpy as np

# Corpus Paralelo: Alineación de Oraciones (Español | Inglés)
CORPUS_PARALELO = [
    ("el perro come", "the dog eats"),
    ("el gato duerme", "the cat sleeps"),
    ("el perro duerme", "the dog sleeps"),
    ("el gato come", "the cat eats"),
]

# La frase que intentaremos traducir
FRASE_FUENTE = "el perro duerme"

# Inicializar contadores para pares de frases (fuente, objetivo)
conteo_pares = {}

# Extraer pares de frases (simulando frases de longitud 1 y 2)
for es_sent, en_sent in CORPUS_PARALELO:
    es_tokens = es_sent.split()
    en_tokens = en_sent.split()

    # Combinaciones de frases de longitud 1 (unigramas)
    for i in range(len(es_tokens)):
        es_phrase = es_tokens[i]
        for j in range(len(en_tokens)):
            en_phrase = en_tokens[j]
            par = (es_phrase, en_phrase)
            conteo_pares[par] = conteo_pares.get(par, 0) + 1
    
    # Combinaciones de frases de longitud 2 (bigramas)
    for i in range(len(es_tokens) - 1):
        es_phrase = " ".join(es_tokens[i:i+2])
        for j in range(len(en_tokens) - 1):
            en_phrase = " ".join(en_tokens[j:j+2])
            par = (es_phrase, en_phrase)
            conteo_pares[par] = conteo_pares.get(par, 0) + 1

# Contar las ocurrencias de cada frase fuente (para el denominador)
conteo_fuente = {}
for (es_phrase, _), count in conteo_pares.items():
    conteo_fuente[es_phrase] = conteo_fuente.get(es_phrase, 0) + count

# Crear la Tabla de Frases (El corazón del Modelo de Traducción SMT)
tabla_frases = {}

for (es_phrase, en_phrase), count_pair in conteo_pares.items():
    count_es = conteo_fuente[es_phrase]
    
    # Probabilidad: P(Objetivo | Fuente)
    probabilidad = count_pair / count_es
    
    if es_phrase not in tabla_frases or probabilidad > tabla_frases[es_phrase][1]:
        # Almacenar solo la traducción más probable para simplificar
        tabla_frases[es_phrase] = (en_phrase, probabilidad)

print("=========================================================")
print("          MODELO DE TRADUCCIÓN SMT (Tabla de Frases)     ")
print("=========================================================")
print("Frases Fuente | Traducción Más Probable (P(Objetivo | Fuente))")
print("-" * 60)
for es_phrase, (en_phrase, prob) in sorted(tabla_frases.items()):
    print(f"{es_phrase.ljust(15)} -> {en_phrase.ljust(15)} ({prob:.2f})")
print("-" * 60)

# Intentar traducir la frase completa (simulación del Modelo de Traducción)
if FRASE_FUENTE in tabla_frases:
    traduccion_encontrada = tabla_frases[FRASE_FUENTE][0]
    prob_traduccion = tabla_frases[FRASE_FUENTE][1]
    
    # En un SMT real, esto se combinaría con el Modelo de Lenguaje P(e)
    # P(e|f) = P(f|e) * P(e)
    
    print(f"Traduciendo: '{FRASE_FUENTE}'")
    print(f"Mejor Traducción Encontrada: '{traduccion_encontrada}'")
    print(f"Probabilidad del Modelo de Traducción P(Objetivo|Fuente): {prob_traduccion:.2f}")
else:
    print(f"La frase '{FRASE_FUENTE}' no se encontró directamente en la tabla.")

