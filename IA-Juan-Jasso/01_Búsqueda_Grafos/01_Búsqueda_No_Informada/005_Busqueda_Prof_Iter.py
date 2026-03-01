# Búsqueda en Profundidad Iterativa (IDS)

def dls_recursivo(grafo, nodo_actual, objetivo, limite_actual, limite_maximo):
    """
    Función auxiliar DLS: Búsqueda en Profundidad Limitada.
    Retorna el nodo objetivo si se encuentra, o None/String si falla.
    """
    if nodo_actual == objetivo:
        return nodo_actual
    
    # Detener la exploración si se alcanza el límite
    if limite_actual == limite_maximo:
        return "LIMITE_ALCANZADO" # Indicador de que solo se detuvo por el límite
    
    # Exploración recursiva
    for vecino in grafo.get(nodo_actual, []):
        resultado = dls_recursivo(grafo, vecino, objetivo, limite_actual + 1, limite_maximo)
        
        # Si encuentra el objetivo, lo propaga hacia arriba
        if resultado and resultado != "LIMITE_ALCANZADO":
            return resultado
            
    return None # Indica que la rama fue explorada completamente y no encontró el objetivo

def ids(grafo, inicio, objetivo, limite_maximo_total):
    """
    Búsqueda en Profundidad Iterativa (IDS).
    Llama a DLS repetidamente con límites crecientes (0, 1, 2, ...).
    """
    print(f"Buscando objetivo '{objetivo}'...")
    
    # 1. Bucle de Iteración: Aumenta el límite de profundidad L
    for limite in range(limite_maximo_total + 1):
        print(f"\n--- Iteración con Límite = {limite} ---")
        
        # 2. Llamada a la Búsqueda en Profundidad Limitada
        resultado = dls_recursivo(grafo, inicio, objetivo, 0, limite)
        
        if resultado == objetivo:
            return f"¡Objetivo '{objetivo}' encontrado en la Iteración {limite} (Profundidad más corta)!"
        
        if resultado == None and limite == limite_maximo_total:
            # Si se exploró todo el grafo hasta el límite máximo y aún no se encuentra
            return "El objetivo no se encontró dentro del límite máximo."
            
    return "Búsqueda terminada."

# Definición del grafo:
mapa = {
    'A': ['B', 'C'], # Nivel 0
    'B': ['D'],      # Nivel 1
    'C': ['E', 'F'], # Nivel 1
    'D': ['G'],      # Nivel 2
    'E': [],
    'F': [],
    'G': []          # Nivel 3 (Objetivo)
}

# El objetivo 'G' se encuentra en la profundidad 3.
LIMITE_MAXIMO_PERMITIDO = 4

print(f"Grafo (Mapa): {mapa}")
resultado_ids = ids(mapa, 'A', 'G', LIMITE_MAXIMO_PERMITIDO)

print("\n" + "=" * 40)
print(f"Resultado final IDS: {resultado_ids}")