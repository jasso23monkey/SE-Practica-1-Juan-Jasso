# Búsqueda en Profundidad Limitada (DLS)

def dls_recursivo(grafo, nodo_actual, objetivo, limite_actual, limite_maximo):
    """
    Función recursiva para la Búsqueda en Profundidad Limitada.
    """
    print(f"  Visitando: {nodo_actual} (Profundidad: {limite_actual})")

    # 1. PRUEBA DE OBJETIVO
    if nodo_actual == objetivo:
        return f"¡Objetivo '{objetivo}' encontrado en profundidad {limite_actual}!"
        
    # 2. PRUEBA DE LÍMITE
    if limite_actual == limite_maximo:
        return "Límite alcanzado, no se encontró el objetivo."
        
    # 3. EXPLORACIÓN RECURSIVA
    for vecino in grafo.get(nodo_actual, []):
        # Llamada recursiva, incrementando la profundidad
        resultado = dls_recursivo(grafo, vecino, objetivo, limite_actual + 1, limite_maximo)
        
        # Si la llamada recursiva encontró el objetivo, se detiene y devuelve el resultado.
        if isinstance(resultado, str) and resultado.startswith("¡Objetivo"):
            return resultado
            
    return "Fallo en la búsqueda (Retroceso)."

# Definición del grafo:
mapa_profundo = {
    'A': ['B', 'C'], # Nivel 0
    'B': ['D'],      # Nivel 1
    'C': ['E', 'F'], # Nivel 1
    'D': ['G'],      # Nivel 2
    'E': [],
    'F': [],
    'G': []          # Nivel 3 (Objetivo)
}

# La profundidad real del objetivo 'G' es 3.
LIMITE_DE_BUSQUEDA = 2 

print(f"Grafo (Mapa): {mapa_profundo}")
print(f"Límite de Profundidad (L): {LIMITE_DE_BUSQUEDA}")
print("-" * 40)

resultado_dls = dls_recursivo(mapa_profundo, 'A', 'G', 0, LIMITE_DE_BUSQUEDA)

print("-" * 40)
print(f"Resultado final DLS: {resultado_dls}")