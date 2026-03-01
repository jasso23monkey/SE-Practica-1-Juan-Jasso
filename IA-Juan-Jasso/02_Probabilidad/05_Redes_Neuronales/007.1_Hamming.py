import numpy as np

# --- 1. Patrones Memorizados (Almacenamiento) ---
# Patrones binarios (longitud 7)
PATRONES = {
    'A': np.array([1, 1, 1, 0, 0, 0, 0]),
    'B': np.array([0, 0, 0, 1, 1, 1, 1])
}

# --- 2. Entrada Ruidosa (Reconocimiento) ---
# Entrada con ruido (un bit cambiado respecto a 'A')
ENTRADA_RUIDOSA = np.array([1, 1, 0, 0, 0, 0, 0])

# --- 3. Función de la Red de Hamming ---

def clasificar_hamming(entrada, patrones):
    """Calcula la distancia de Hamming a cada patrón memorizado."""
    
    distancias = {}
    
    for etiqueta, patron in patrones.items():
        # La distancia de Hamming es el número de posiciones donde los bits difieren.
        # Se calcula sumando los valores booleanos (True=1, False=0) de la diferencia.
        diferencias = np.abs(entrada - patron)
        distancia_h = np.sum(diferencias)
        distancias[etiqueta] = distancia_h
        
    # La clasificación es el patrón con la distancia MÍNIMA
    bmu = min(distancias, key=distancias.get)
    
    return distancias, bmu

# --- 4. Ejecución ---

distancias, clasificacion = clasificar_hamming(ENTRADA_RUIDOSA, PATRONES)

print("=============================================")
print("          RED DE HAMMING (CLASIFICACIÓN)     ")
print("=============================================")
print(f"Patrón de Entrada: {ENTRADA_RUIDOSA}")
print("-" * 50)
for etiqueta, dist in distancias.items():
    print(f"Distancia al Patrón '{etiqueta}': {dist}")

print(f"\nClasificación (BMU): El patrón más cercano es '{clasificacion}'.")