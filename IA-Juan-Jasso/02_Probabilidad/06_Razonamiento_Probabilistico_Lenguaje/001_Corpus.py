import numpy as np
import collections # Usamos collections.defaultdict para simplificar los conteos

# --- 1. El Corpus (Colección de Textos) ---
corpus_texto = [
    "El sol brilla en la mañana y el dios no.",
    "La mañana es fresca y el sol es amarillo.",
    "El perro corre tras la bola. No hay sol porque es el parque."
]

# --- 2. Preprocesamiento y Tokenización ---

def tokenizar_corpus(textos):
    """Limpia, convierte a minúsculas y tokeniza el corpus."""
    tokens = []
    for texto in textos:
        # Limpieza: Convertir a minúsculas y eliminar signos de puntuación
        texto_limpio = texto.lower().replace('.', '').replace(',', '')
        
        # Tokenización: Dividir en palabras
        palabras = texto_limpio.split()
        
        # Opcional: Añadir marcadores de inicio/fin de frase (útil en MPL reales)
        tokens.extend(["<INI>"] + palabras + ["<FIN>"])
    return tokens

TOKENS = tokenizar_corpus(corpus_texto)
VOCABULARIO = sorted(list(set(TOKENS)))

print("====================================================")
print("     PROCESAMIENTO DE CORPUS PARA BIGRAMAS (N=2)    ")
print("====================================================")
print(f"Número total de tokens: {len(TOKENS)}")
print(f"Vocabulario (muestra): {VOCABULARIO[:5]}...")
print("-" * 50)

# Contadores
conteo_unigramas = collections.defaultdict(int)
conteo_bigramas = collections.defaultdict(int)

# Realizar conteos
for i, token in enumerate(TOKENS):
    conteo_unigramas[token] += 1
    
    # Bigrama: (palabra_anterior, palabra_actual)
    if i > 0:
        bigrama = (TOKENS[i-1], token)
        conteo_bigramas[bigrama] += 1

# Mostrar algunos conteos
print("Conteo de Unigramas (muestra):")
for k, v in list(conteo_unigramas.items())[:5]:
    print(f"  '{k}': {v} veces")

print("\nConteo de Bigramas (muestra):")
for k, v in list(conteo_bigramas.items())[:5]:
    print(f"  '{k[0]} {k[1]}': {v} veces")
print("-" * 50)

def probabilidad_bigrama(w_anterior, w_siguiente, unigramas, bigramas):
    """Estima la probabilidad condicional P(w_siguiente | w_anterior)."""
    
    # Contar la ocurrencia de la palabra anterior (denominador)
    conteo_anterior = unigramas[w_anterior]
    
    # Contar la ocurrencia del par (numerador)
    conteo_par = bigramas[(w_anterior, w_siguiente)]
    
    if conteo_anterior == 0:
        # Manejo de "token desconocido" (problema de sparsity/escasez)
        return 0.0
    else:
        probabilidad = conteo_par / conteo_anterior
        return probabilidad

# --- Pruebas del Modelo de Lenguaje ---
palabra_base = "el"
siguientes_candidatas = ["sol", "perro", "día"]

print(f"Probabilidades de P(? | '{palabra_base}'):")
for candidata in siguientes_candidatas:
    prob = probabilidad_bigrama(palabra_base, candidata, conteo_unigramas, conteo_bigramas)
    print(f"  P('{candidata}' | '{palabra_base}') = {prob:.4f}")

# --- Ejemplo de Secuencia no vista (El problema de la escasez) ---
prob_cero = probabilidad_bigrama("perro", "mañana", conteo_unigramas, conteo_bigramas)
print(f"\nProbabilidad de una secuencia no vista P('mañana' | 'perro'): {prob_cero:.4f}")