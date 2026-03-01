# Búsqueda Voraz Primero (Greedy Best-First Search) con Heurísticas

import heapq

def busqueda_voraz(grafo, heuristica, inicio, objetivo):
    """
    Implementa la Búsqueda Voraz, usando la heurística h(n) como prioridad.
    La prioridad en la cola es SOLO el valor h(n).
    """
    # Cola de prioridad: (h(n), nodo)
    cola_prioridad = [(heuristica[inicio], inicio)]
    visitados = {inicio}
    
    while cola_prioridad:
        # Extrae el nodo con el valor heurístico MÁS BAJO
        (h_costo, nodo_actual) = heapq.heappop(cola_prioridad)
        
        print(f"  Visitando: {nodo_actual} (h={h_costo})")
        
        if nodo_actual == objetivo:
            return f"¡Objetivo '{objetivo}' encontrado!"
        
        # Explora vecinos
        for vecino in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                # La prioridad es ÚNICAMENTE la heurística del vecino: h(vecino)
                h_vecino = heuristica.get(vecino, float('inf')) 
                heapq.heappush(cola_prioridad, (h_vecino, vecino))
                
    return "Fallo en la búsqueda: No hay camino."

# Definición del Grafo y la Heurística
mapa = {
    'A': ['B', 'C'],
    'B': ['D'],
    'C': ['E'],
    'D': ['E'],
    'E': ['F']  # Objetivo
}

# Valores Heurísticos h(n): Estimación de la distancia al Objetivo ('F')
# Nota: La heurística para 'C' es 1, mientras que para 'B' es 4.
# El algoritmo elegirá 'C' antes que 'B' porque PARECE más prometedor.
heuristica_a_f = {
    'A': 5,
    'B': 4,
    'C': 1,  # Nodo más prometedor (menor h)
    'D': 2,
    'E': 1,
    'F': 0   # El objetivo siempre tiene h=0
}

INICIO = 'A'
OBJETIVO = 'F'

print(f"Grafo: {mapa}")
print(f"Heurísticas (Estimación a 'F'): {heuristica_a_f}")
print("-" * 50)
print("Búsqueda Voraz (A → F):")
resultado = busqueda_voraz(mapa, heuristica_a_f, INICIO, OBJETIVO)

print("-" * 50)
print("Resultado final: {resultado}")