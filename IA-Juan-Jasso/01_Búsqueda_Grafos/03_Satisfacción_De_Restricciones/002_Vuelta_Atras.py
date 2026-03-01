# Búsqueda de Vuelta Atrás (Backtracking Search) - Básico

# --- 1. DEFINICIÓN DEL CSP ---
VARIABLES = ['A', 'B', 'C'] 

# Dominios: Ambos países pueden ser Rojo o Verde
DOMINIOS = {
    'A': ['Rojo', 'Verde'],
    'B': ['Rojo', 'Verde'],
    'C': ['Rojo', 'Verde']
}

# Restricciones (Vecinos): A != B, A != C
RESTRICCIONES_VECINOS = [('A', 'B'), ('A', 'C')]

# --- 2. FUNCIÓN DE VERIFICACIÓN DE RESTRICCIONES ---

def es_consistente(variable, valor, asignacion):
    """
    Verifica si asignar 'valor' a 'variable' viola alguna restricción 
    con las asignaciones que ya están hechas.
    """
    for v1, v2 in RESTRICCIONES_VECINOS:
        # Chequea la restricción (v1 != v2)
        
        # 1. Caso: La variable actual es v1 y v2 ya está asignada
        if v1 == variable and v2 in asignacion:
            if valor == asignacion[v2]:
                return False  # Conflicto: el valor es igual al del vecino asignado

        # 2. Caso: La variable actual es v2 y v1 ya está asignada
        elif v2 == variable and v1 in asignacion:
            if valor == asignacion[v1]:
                return False  # Conflicto
                
    return True

# --- 3. ALGORITMO PRINCIPAL DE BACKTRACKING ---

def backtracking_search(asignacion):
    """
    Implementa el algoritmo recursivo de Búsqueda de Vuelta Atrás.
    """
    # CASO BASE: Si todas las variables tienen una asignación, hemos terminado.
    if len(asignacion) == len(VARIABLES):
        return asignacion

    # 1. SELECCIÓN DE VARIABLE (Sin heurística, se elige la primera no asignada)
    variable = [v for v in VARIABLES if v not in asignacion][0]

    # 2. INTENTAR VALORES
    for valor in DOMINIOS[variable]:
        
        # 3. VERIFICACIÓN: ¿El valor es consistente con las restricciones?
        if es_consistente(variable, valor, asignacion):
            
            # Asignación: Añadir el valor a la solución parcial
            asignacion[variable] = valor
            
            # 4. LLAMADA RECURSIVA: Continuar la búsqueda
            resultado = backtracking_search(asignacion)
            
            if resultado is not None:
                return resultado # Éxito: Propagar la solución
            
            # 5. VUELTA ATRÁS (Backtrack): Deshacer la asignación
            # Si la rama falló, borrar la asignación para probar el siguiente valor
            del asignacion[variable]
            
    return None # Fallo: Si todos los valores fallaron, volver al paso anterior

# ===================================================
# --- EJECUCIÓN DEL CSP ---
# ===================================================

print("Iniciando Búsqueda de Vuelta Atrás (Básica) para el Coloreado...")
solucion = backtracking_search({})

print("-" * 50)
if solucion:
    print("¡SOLUCIÓN ENCONTRADA!")
    print(f"  Asignaciones: {solucion}")
    print("\nLa búsqueda probó valores secuencialmente (A, luego B, luego C) hasta encontrar la primera solución.")
else:
    print("No se pudo encontrar una solución con los dominios dados.")