# Búsqueda de Costo Uniforme (UCS)

import heapq

def ucs(grafo, inicio, objetivo):
    """
    Implementa el algoritmo de Búsqueda de Costo Uniforme (UCS).
    Encuentra la ruta con el costo acumulado más bajo.
    """
    # La cola de prioridad almacenará tuplas: (costo_acumulado, nodo_actual)
    cola_prioridad = [(0, inicio)] 
    
    # Almacena el costo más bajo encontrado hasta ahora para llegar a cada nodo
    costos = {inicio: 0}
    
    # Almacena el camino para reconstruir la ruta (costo_nodo: padre_nodo)
    padres = {inicio: None} 
    
    while cola_prioridad:
        # Extrae el nodo con el costo ACUMULADO más bajo (gracias a heapq)
        (costo_actual, nodo_actual) = heapq.heappop(cola_prioridad)
        
        # Condición de Éxito
        if nodo_actual == objetivo:
            return f"¡Objetivo '{objetivo}' encontrado con costo {costo_actual}!"
        
        # Exploración
        for vecino, costo_arista in grafo.get(nodo_actual, {}).items():
            # Calcula el nuevo costo total para llegar al vecino a través del nodo actual
            nuevo_costo = costo_actual + costo_arista
            
            # Relajación: Si encontramos un camino más barato, lo actualizamos
            if vecino not in costos or nuevo_costo < costos[vecino]:
                costos[vecino] = nuevo_costo
                padres[vecino] = nodo_actual
                # Agrega o actualiza el nodo en la cola de prioridad
                heapq.heappush(cola_prioridad, (nuevo_costo, vecino))
                
    return f"Objetivo '{objetivo}' no alcanzable"

# Definición del grafo: Nodo -> {Vecino: Costo_Arista}
# A -> C tiene un costo más alto (4) que A -> B (1), lo que afecta la ruta
mapa_con_costos = {
    'A': {'B': 1, 'C': 4},
    'B': {'D': 5, 'E': 2},
    'C': {'F': 3},
    'D': {'G': 1},
    'E': {'G': 8}, # Ruta B->E->G (1+2+8=11) es más cara que B->D->G (1+5+1=7)
    'F': {},
    'G': {} # Objetivo
}

resultado_ucs = ucs(mapa_con_costos, 'A', 'G')

print("Grafo con costos (Mapa):")
for nodo, vecinos in mapa_con_costos.items():
    print(f"  {nodo}: {vecinos}")
print("-" * 30)
print(f"Resultado de la búsqueda UCS (A → G): {resultado_ucs}")