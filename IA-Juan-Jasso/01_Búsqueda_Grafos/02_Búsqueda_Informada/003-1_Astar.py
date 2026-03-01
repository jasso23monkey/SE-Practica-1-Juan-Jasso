# Búsqueda A* (A-Star)

import heapq

def busqueda_a_estrella(grafo, costos, heuristica, inicio, objetivo):
    """
    Implementa el algoritmo A* usando una cola de prioridad.
    """
    # Cola de prioridad: (f(n), nodo)
    cola_prioridad = [(heuristica[inicio], inicio)]
    
    # g(n): Costo real del inicio al nodo actual
    g_costos = {inicio: 0} 
    
    # Almacena el nodo padre para reconstruir la ruta
    padres = {inicio: None}
    
    while cola_prioridad:
        # Extrae el nodo con el menor f(n) estimado
        (costo, nodo_actual) = heapq.heappop(cola_prioridad)
        
        if nodo_actual == objetivo:
            return f"¡Objetivo '{objetivo}' encontrado! Costo real: {g_costos[objetivo]}"
        
        # Explora vecinos
        for vecino, costo_arista in grafo.get(nodo_actual, {}).items():
            # g(vecino) = g(nodo_actual) + costo_arista
            nuevo_g_costo = g_costos[nodo_actual] + costo_arista
            
            # Si se encuentra un camino mejor (menor g(n)), o es la primera vez que se visita
            if vecino not in g_costos or nuevo_g_costo < g_costos[vecino]:
                g_costos[vecino] = nuevo_g_costo
                padres[vecino] = nodo_actual
                
                # f(n) = g(n) + h(n)
                h_vecino = heuristica.get(vecino, float('inf'))
                f_vecino = nuevo_g_costo + h_vecino
                
                # Agrega el vecino a la cola con su f(n) como prioridad
                heapq.heappush(cola_prioridad, (f_vecino, vecino))
                
    return "Fallo en la búsqueda: No hay camino."

# Definición del Grafo con Costos (Arista: Costo)
mapa_costos = {
    'A': {'B': 1, 'C': 4},
    'B': {'D': 5, 'E': 2},
    'C': {'F': 3},
    'D': {'G': 1},
    'E': {'G': 8}, 
    'F': {},
    'G': {} # Objetivo
}

# Heurística h(n) (Estimación de costo del nodo al Objetivo 'G')
heuristica_g = {
    'A': 8, 'B': 5, 'C': 5, 'D': 1, 'E': 2, 'F': 4, 'G': 0
}

INICIO = 'A'
OBJETIVO = 'G'

print(f"Grafo (Costos Reales): {mapa_costos}")
print(f"Heurística h(n) a 'G': {heuristica_g}")
print("-" * 50)
print(f"Búsqueda A* ({INICIO} → {OBJETIVO}):")
resultado = busqueda_a_estrella(mapa_costos, mapa_costos, heuristica_g, INICIO, OBJETIVO)

print("-" * 50)
print(f"Resultado: {resultado}")