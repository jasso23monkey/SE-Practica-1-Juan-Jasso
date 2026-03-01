# Problema de Satisfacción de Restricciones (CSP) - Coloreado de Mapa Simple

# --- 1. DEFINICIÓN DEL CSP ---

# Variables (Países)
VARIABLES = ['A', 'B', 'C'] 

# Dominios (Colores disponibles)
DOMINIOS = {
    'A': ['Rojo', 'Verde'],
    'B': ['Rojo', 'Verde'],
    'C': ['Rojo', 'Verde']
}

# Restricciones (Vecinos adyacentes: A != B, A != C)
RESTRICCIONES_VECINOS = [
    ('A', 'B'),
    ('A', 'C')
    # Nota: B y C no son vecinos en este ejemplo.
]

# --- 2. FUNCIÓN DE VERIFICACIÓN DE RESTRICCIONES ---

def es_consistente(variable, valor, asignacion):
    """
    Verifica si asignar 'valor' a 'variable' es consistente con las
    asignaciones ya hechas (en el diccionario 'asignacion').
    """
    for v1, v2 in RESTRICCIONES_VECINOS:
        # 1. Chequear restricciones donde la 'variable' es la primera
        if v1 == variable and v2 in asignacion:
            if valor == asignacion[v2]:
                return False  # El color es el mismo que el vecino ya asignado

        # 2. Chequear restricciones donde la 'variable' es la segunda
        elif v2 == variable and v1 in asignacion:
            if valor == asignacion[v1]:
                return False  # El color es el mismo que el vecino ya asignado
                
    return True # Es consistente con todas las asignaciones existentes

# --- 3. ALGORITMO DE BÚSQUEDA CON VUELTA ATRÁS ---

def backtracking_search(asignacion):
    """
    Implementa la Búsqueda con Vuelta Atrás recursiva para resolver el CSP.
    """
    # CASO BASE: Si todas las variables están asignadas, hemos encontrado una solución.
    if len(asignacion) == len(VARIABLES):
        return asignacion

    # 1. SELECCIÓN DE VARIABLE (Elegir la primera variable no asignada)
    variable = [v for v in VARIABLES if v not in asignacion][0]

    # 2. INTENTAR VALORES
    for valor in DOMINIOS[variable]:
        
        # 3. VERIFICACIÓN DE CONSISTENCIA
        if es_consistente(variable, valor, asignacion):
            
            # Asignación exitosa: Añadir y continuar la búsqueda recursivamente
            asignacion[variable] = valor
            
            resultado = backtracking_search(asignacion)
            
            if resultado is not None:
                return resultado # ¡Solución encontrada! Devolver el resultado

            # 4. VUELTA ATRÁS (Backtrack)
            # Si la recursión no encontró solución, deshacer la asignación
            del asignacion[variable]
            
    return None # No se encontró solución para esta rama

# ===================================================
# --- EJECUCIÓN DEL CSP ---
# ===================================================

print("Iniciando Búsqueda con Vuelta Atrás para el Coloreado de Mapas...")
solucion = backtracking_search({})

print("-" * 50)
if solucion:
    print("¡SOLUCIÓN ENCONTRADA!")
    for pais, color in solucion.items():
        print(f"  {pais} ({'Argentina' if pais=='A' else 'Brasil' if pais=='B' else 'Chile'}): {color}")
    print("\nVerificación de Restricciones:")
    print(f"  A ({solucion['A']}) ≠ B ({solucion['B']})? -> {'Sí' if solucion['A'] != solucion['B'] else 'No'}")
    print(f"  A ({solucion['A']}) ≠ C ({solucion['C']})? -> {'Sí' if solucion['A'] != solucion['C'] else 'No'}")
else:
    print("No se pudo encontrar una solución con los dominios dados.")