import numpy as np

# --- 1. El Corpus y la Consulta ---
# Documentos (D)
D1 = "el perro come y juega en el parque"
D2 = "el gato duerme en la cama, no juega"
D3 = "el perro duerme en el parque con el gato"
DOCUMENTOS = [D1, D2, D3]

# Consulta (Q)
CONSULTA = "perro juega parque"

# Lista de palabras a ignorar (stop words) para simplificar el vocabulario
STOP_WORDS = set(["el", "la", "y", "en", "no", "con"])

def preprocesar(texto):
    """Limpia el texto, elimina stop words y tokeniza."""
    tokens = [t for t in texto.lower().split() if t not in STOP_WORDS]
    return tokens

# Tokens de todos los documentos y la consulta
TOKENS_DOCUMENTOS = [preprocesar(d) for d in DOCUMENTOS]
TOKENS_CONSULTA = preprocesar(CONSULTA)

# Construir Vocabulario (todas las palabras únicas)
VOCABULARIO = sorted(list(set(
    t for doc in TOKENS_DOCUMENTOS for t in doc
) | set(TOKENS_CONSULTA)))

print("=====================================================")
print("  RECUPERACIÓN DE DATOS (VSM, TF-IDF y Coseno)       ")
print("=====================================================")
print(f"Vocabulario: {VOCABULARIO}")
print("-" * 50)

N_DOCS = len(DOCUMENTOS)
N_VOCAB = len(VOCABULARIO)

# Mapeo de vocabulario a índice
vocab_map = {word: i for i, word in enumerate(VOCABULARIO)}

# A. Cálculo de TF (Documentos)
TF_docs = np.zeros((N_DOCS, N_VOCAB))
for i, tokens in enumerate(TOKENS_DOCUMENTOS):
    for token in tokens:
        if token in vocab_map:
            TF_docs[i, vocab_map[token]] += 1

# B. Cálculo de IDF (Frecuencia Inversa de Documento)
# Df: Número de documentos que contienen cada término
df = np.sum(TF_docs > 0, axis=0) 
# IDF = log(N / Df) + 1 (Fórmula clásica suave)
IDF = np.log(N_DOCS / df) + 1

# C. Cálculo de TF-IDF (Vectores de Documentos)
TFIDF_docs = TF_docs * IDF 

# D. Cálculo de TF-IDF (Vector de Consulta)
# Simplemente se usan las frecuencias de la consulta multiplicadas por el IDF global
TF_query = np.zeros(N_VOCAB)
for token in TOKENS_CONSULTA:
    if token in vocab_map:
        TF_query[vocab_map[token]] += 1
        
TFIDF_query = TF_query * IDF

def similitud_coseno(vec_a, vec_b):
    """Calcula la similitud de coseno entre dos vectores."""
    dot_product = np.dot(vec_a, vec_b)
    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot_product / (norm_a * norm_b)

# Calcular la similitud para cada documento
relevancias = {}
for i, doc in enumerate(DOCUMENTOS):
    sim = similitud_coseno(TFIDF_query, TFIDF_docs[i, :])
    relevancias[f"D{i+1}"] = sim

# Ordenar los documentos por relevancia descendente
resultados_ordenados = sorted(relevancias.items(), key=lambda item: item[1], reverse=True)

# --- 5. Resultados ---

print("Pesos TF-IDF (Fragmento):")
print(f"  Consulta: {TFIDF_query.round(2)}")
print(f"  D1 (Perro come...): {TFIDF_docs[0, :].round(2)}")
print(f"  D2 (Gato duerme...): {TFIDF_docs[1, :].round(2)}")
print("-" * 50)

print(f"Consulta: '{CONSULTA}'")
print("\nRESULTADOS DE RECUPERACIÓN (Ordenados por Similitud):")
for doc_id, sim in resultados_ordenados:
    print(f"  {doc_id} (Similitud: {sim:.4f})")