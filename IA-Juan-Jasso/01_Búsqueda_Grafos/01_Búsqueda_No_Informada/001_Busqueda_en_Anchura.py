# Búsqueda en Grafos: Búsqueda Primero en Amplitud (BFS)

from collections import deque

def bfs(grafo, inicio, objetivo):
    """
    Implementa BFS para encontrar la ruta más corta (en número de nodos) entre dos nodos.
    """
    cola = deque([inicio])  # 1. Inicializa la cola con el nodo de inicio
    visitados = {inicio}    # 2. Inicializa el conjunto de nodos visitados
    
    # 3. Mientras la cola no esté vacía (es decir, quedan nodos por explorar)
    while cola:
        nodo_actual = cola.popleft() # 4. Saca el primer nodo de la cola (¡Amplitud!)
        
        if nodo_actual == objetivo:
            return f"¡Objetivo '{objetivo}' encontrado!"
            
        # 5. Explora los vecinos
        for vecino in grafo.get(nodo_actual, []):
            if vecino not in visitados:
                visitados.add(vecino)
                cola.append(vecino) # 6. Agrega los vecinos no visitados al final de la cola
                
    return f"Objetivo '{objetivo}' no alcanzable"

# Definición de un grafo simple
mapa_simple = {
    'A': ['B', 'C'], # Desde A puedes ir a B y C
    'B': ['D'],
    'C': ['E', 'F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': [] # Objetivo
}

resultado_bfs = bfs(mapa_simple, 'A', 'G')

print(f"Grafo (Mapa): {mapa_simple}")
print(f"Resultado de la busqueda BFS (A → G): {resultado_bfs}")