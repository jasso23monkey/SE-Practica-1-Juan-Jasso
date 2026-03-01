# Búsqueda en Profundidad (DFS)

def dfs(grafo, inicio, objetivo):
    """
    Implementa el algoritmo de Búsqueda Primero en Profundidad (DFS).
    Prioriza explorar tan profundo como sea posible en una rama antes de retroceder.
    """
    # Usamos una lista como Pila (Stack). La pila funciona LIFO (Last-In, First-Out).
    pila = [inicio]
    visitados = {inicio}
    
    while pila:
        # 1. Saca el ÚLTIMO elemento de la pila (LIFO: Profundidad)
        nodo_actual = pila.pop()
        
        if nodo_actual == objetivo:
            return f"¡Objetivo '{objetivo}' encontrado!"
        
        # 2. Explora los vecinos
        # Recorremos los vecinos en orden inverso para que se inserten en orden
        # que se sacarán (solo para asegurar un orden de exploración predecible)
        for vecino in reversed(grafo.get(nodo_actual, [])):
            if vecino not in visitados:
                visitados.add(vecino)
                # 3. Agrega el vecino a la Pila (será el siguiente a explorar)
                pila.append(vecino)
                
    return f"Objetivo '{objetivo}' no alcanzable"

# Definición del grafo simple (Mismo grafo de BFS)
mapa_simple = {
    'A': ['B', 'C'], 
    'B': ['D'],
    'C': ['E', 'F'],
    'D': [],
    'E': ['G'],
    'F': [],
    'G': [] # Objetivo
}

resultado_dfs = dfs(mapa_simple, 'A', 'G')

print(f"Grafo (Mapa): {mapa_simple}")
print(f"Resultado de la búsqueda DFS (A → G): {resultado_dfs}")