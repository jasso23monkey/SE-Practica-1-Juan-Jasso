# Búsqueda Bidireccional (Bidirectional Search)

from collections import deque

def revertir_grafo(grafo_dirigido):
    """Crea una versión del grafo con las aristas invertidas."""
    grafo_revertido = {nodo: [] for nodo in grafo_dirigido}
    for nodo, vecinos in grafo_dirigido.items():
        for vecino in vecinos:
            # Si el vecino no existe como llave principal, lo agregamos
            if vecino not in grafo_revertido:
                grafo_revertido[vecino] = []
            # La arista revertida es: Vecino apunta a Nodo (padre original)
            grafo_revertido[vecino].append(nodo)
    return grafo_revertido

def buscar_bidireccionalmente(grafo, inicio, objetivo):
    if inicio == objetivo:
        return f"Inicio y Objetivo son el mismo: {inicio}."

    # Pre-calcular el grafo revertido para la búsqueda hacia atrás
    grafo_revertido = revertir_grafo(grafo)
    
    # Colas y conjuntos
    cola_f = deque([inicio])
    cola_b = deque([objetivo])
    visitados_f = {inicio}
    visitados_b = {objetivo}
    padres_f = {inicio: None}
    padres_b = {objetivo: None}
    
    while cola_f and cola_b:
        # 1. Expandir hacia adelante (usando el grafo original)
        nodo_interseccion = expandir_paso(grafo, cola_f, visitados_f, padres_f, visitados_b)
        if nodo_interseccion:
            return reconstruir_ruta(padres_f, padres_b, nodo_interseccion, inicio, objetivo)

        # 2. Expandir hacia atrás (usando el grafo revertido)
        nodo_interseccion = expandir_paso(grafo_revertido, cola_b, visitados_b, padres_b, visitados_f)
        if nodo_interseccion:
            return reconstruir_ruta(padres_f, padres_b, nodo_interseccion, inicio, objetivo)

    return "Fallo en la búsqueda: No hay camino."

def expandir_paso(grafo_usar, cola_act, visitados_act, padres_act, visitados_op):
    """Realiza un solo paso de expansión para una de las búsquedas."""
    if not cola_act:
        return None
        
    nodo_actual = cola_act.popleft()
    
    # Chequeo de intersección (el nodo actual fue visitado por la búsqueda opuesta)
    if nodo_actual in visitados_op:
        return nodo_actual # ¡Intersección encontrada!
        
    # Explora vecinos
    for vecino in grafo_usar.get(nodo_actual, []):
        if vecino not in visitados_act:
            visitados_act.add(vecino)
            padres_act[vecino] = nodo_actual
            cola_act.append(vecino)
            
    return None

def reconstruir_ruta(padres_f, padres_b, interseccion, inicio, objetivo):
    """Combina los dos caminos encontrados en el nodo de intersección."""
    # Camino hacia adelante (de inicio a intersección)
    camino_f = []
    actual = interseccion
    while actual is not None:
        camino_f.append(actual)
        actual = padres_f.get(actual)
    camino_f.reverse()

    # Camino hacia atrás (de intersección a objetivo)
    camino_b = []
    actual = interseccion
    # El primer nodo (intersección) ya está en camino_f, así que avanzamos al padre
    actual = padres_b.get(interseccion)
    while actual is not None:
        camino_b.append(actual)
        actual = padres_b.get(actual)
    
    # La ruta se forma: (camino_f) + (camino_b en orden inverso)
    ruta_final = camino_f + list(reversed(camino_b))
    
    # A veces el nodo de intersección puede repetirse al unir las listas, se limpia:
    if len(ruta_final) > 1 and ruta_final[-1] == ruta_final[-2]:
        ruta_final.pop()

    return f"¡Ruta encontrada! Intersección en '{interseccion}'. Ruta: {' → '.join(ruta_final)}"


# Definición del grafo simple (dirigido)
mapa = {
    'A': ['B', 'G'],
    'B': ['C', 'H'],
    'C': ['D'],
    'D': ['E'],
    'E': ['F'],
    'F': ['I'],
    'G': ['J'],
    'H': ['K', 'L'],
    'I': [],
    'J': [],
    'K': ['M'],
    'L': ['M'],
    'M': [] # Objetivo
}
INICIO = 'A'
OBJETIVO = 'M'

# Verificación de la reversión (opcional, para entender el cambio)
# print("Grafo Revertido (Para búsqueda desde M):")
# print(revertir_grafo(mapa))

print(f"Grafo (Mapa): {mapa}")
print("-" * 50)
resultado = buscar_bidireccionalmente(mapa, INICIO, OBJETIVO)

print(f"Búsqueda Bidireccional ({INICIO} → {OBJETIVO}):")
print(resultado)