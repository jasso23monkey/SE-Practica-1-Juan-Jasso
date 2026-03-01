import itertools

# --- 1. DEFINICIÓN DEL CSP ---
VARIABLES = ['V1', 'V2', 'V3', 'V4']
DOMINIO = [1, 2] # Dominio pequeño para la simulación

# Grafo cíclico: V1-V2, V2-V3, V3-V4, V4-V1
RESTRICCIONES_VECINOS = [('V1', 'V2'), ('V2', 'V3'), ('V3', 'V4'), ('V4', 'V1')]
# Condición: V_i != V_j

# --- 2. IDENTIFICACIÓN DEL CORTE ---
CUTSET_W = ['V1']
RESTO_V_W = ['V2', 'V3', 'V4'] 

# --- 3. FUNCIONES DE COMPROBACIÓN ---

def es_consistente(asignacion):
    """Verifica si la asignación es consistente con todas las restricciones binarias."""
    for v1, v2 in RESTRICCIONES_VECINOS:
        if v1 in asignacion and v2 in asignacion:
            if asignacion[v1] == asignacion[v2]:
                return False
    return True

def resolver_arbol(asignacion_corte):
    """
    Simulación de la resolución rápida y eficiente del CSP restante (V2, V3, V4).
    En un algoritmo real, esto sería un pase de Consistencia de Arco (AC)
    seguido de una asignación lineal.
    """
    solucion_arbol = dict(asignacion_corte)
    
    # El árbol (V2-V3-V4) con V1 fijado
    
    # Lógica de asignación lineal (como si fuera AC y luego DFS/BFS)
    for v in RESTO_V_W:
        encontrado = False
        for valor in DOMINIO:
            # Intentar el valor, verificando solo las restricciones con vecinos
            temp_asignacion = solucion_arbol.copy()
            temp_asignacion[v] = valor
            
            if es_consistente(temp_asignacion):
                solucion_arbol[v] = valor
                encontrado = True
                break
        
        if not encontrado:
            return None # La asignación del corte falló en el árbol
            
    return solucion_arbol

# --- 4. ALGORITMO PRINCIPAL DE ACONDICIONAMIENTO DEL CORTE ---

def cutset_conditioning():
    
    # Búsqueda con Vuelta Atrás sobre el CUTSET_W
    # Generamos todas las combinaciones posibles de asignaciones para V1
    
    # Esto simula la complejidad d^|W| (2^1 = 2 combinaciones)
    for valores_corte in itertools.product(DOMINIO, repeat=len(CUTSET_W)):
        
        asignacion_corte = {var: val for var, val in zip(CUTSET_W, valores_corte)}
        
        print(f"\nIntentando asignación de Corte W: {asignacion_corte}")

        # 1. Comprobar la consistencia interna del corte (trivial aquí, solo V1)
        if not es_consistente(asignacion_corte):
            continue 

        # 2. Intentar resolver el Árbol restante (V-W)
        solucion_final = resolver_arbol(asignacion_corte)
        
        if solucion_final is not None:
            return solucion_final
            
    return None

# --- Ejecución ---
solucion = cutset_conditioning()

print("\n" + "="*50)
if solucion:
    print("Solución Encontrada por Acondicionamiento del Corte:")
    print(f"   Solución: {solucion}")
else:
    print("No se encontró solución.")