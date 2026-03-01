# Heurísticas: Cálculo de la Estimación h(n)
import math

def calcular_heuristica_euclidiana(punto_actual, punto_objetivo):
    """
    Calcula la distancia Euclidiana (línea recta) entre dos puntos.
    Esta es la función heurística h(n).
    h(n) = sqrt((x2 - x1)^2 + (y2 - y1)^2)
    """
    x1, y1 = punto_actual
    x2, y2 = punto_objetivo
    
    # Diferencia de coordenadas
    dx = x2 - x1
    dy = y2 - y1
    
    # Aplicación de la fórmula de distancia
    distancia = math.sqrt(dx**2 + dy**2)
    return distancia

# 1. Definición del Objetivo
OBJETIVO = (10, 5) # Coordenadas (x, y) del destino final

# 2. Definición de los Nodos (Ciudades) con sus coordenadas
puntos_de_mapa = {
    'Ciudad A': (3, 8),
    'Ciudad B': (12, 4), # Debería ser la más cercana
    'Ciudad C': (1, 1),
    'Ciudad D': (7, 6)
}

print(f"Objetivo (Fin del viaje): {OBJETIVO}")
print("-" * 40)
print("Cálculo de la Heurística h(n) para cada ciudad:")

# 3. Calcular la heurística h(n) para cada punto
resultados = {}
for nombre, coords in puntos_de_mapa.items():
    h_n = calcular_heuristica_euclidiana(coords, OBJETIVO)
    resultados[nombre] = h_n
    print(f"  h({nombre} {coords}): {h_n:.2f}")

print("-" * 40)

# 4. Determinación del nodo más prometedor
nodo_mas_prometedor = min(resultados, key=resultados.get)
menor_h = resultados[nodo_mas_prometedor]

print(f"El nodo más prometedor es: {nodo_mas_prometedor}")
print(f"Con la menor heurística (estimación de costo): {menor_h:.2f}")