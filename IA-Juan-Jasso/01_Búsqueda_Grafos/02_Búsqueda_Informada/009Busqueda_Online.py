import math

# --- 1. CONFIGURACIÓN DEL ENTORNO ---
# Grafo: {Nodo: {Vecino: Costo_Real}}
GRAFO_COSTOS = {
    'A': {'B': 1},  
    'B': {'A': 1, 'C': 2},
    'C': {}  # Objetivo, sin salidas
}

# Heurísticas Iniciales (El mapa interno del agente)
# El agente comienza con estas estimaciones iniciales de costo al objetivo.
heuristica = {
    'A': 3,
    'B': 1,
    'C': 0   # El objetivo siempre tiene h=0
}

INICIO = 'A'
OBJETIVO = 'C'
ruta_tomada = []
costo_real_acumulado = 0

# --- 2. FUNCIÓN DE DECISIÓN LRTA* ---
def lrta_star_decision(nodo_actual, h_table, grafo):
    """
    Simula un paso del algoritmo LRTA*: 
    1. Evalúa los sucesores (f(S') = costo + h(S')).
    2. Actualiza la heurística del nodo actual (h(S)).
    3. Devuelve el mejor sucesor para moverse.
    """
    sucesores = grafo.get(nodo_actual, {})
    if not sucesores:
        return None, float('inf')  # Nodo sin salida o objetivo

    mejores_opciones = []
    
    # a) Evaluar Sucesores
    for sucesor, costo_real in sucesores.items():
        # f(S') = costo(S, S') + h(S')
        f_costo = costo_real + h_table.get(sucesor, float('inf')) 
        mejores_opciones.append((f_costo, sucesor, costo_real))
        
    # Encontrar la opción con el menor f_costo
    mejor_f, mejor_sucesor, costo_movimiento = min(mejores_opciones, key=lambda x: x[0])
    
    # b) Actualizar Heurística del Nodo Actual
    # h(S) <- min(costo(S, S') + h(S'))
    h_table[nodo_actual] = mejor_f
    
    return mejor_sucesor, costo_movimiento

# =================================================================
# --- SIMULACIÓN DE BÚSQUEDA ONLINE ---
# =================================================================

nodo_actual = INICIO

print("--- Búsqueda Online LRTA* ---")
print(f"Objetivo: {OBJETIVO}. Heurísticas iniciales: {dict(heuristica)}")
print("-" * 50)

while nodo_actual != OBJETIVO and nodo_actual is not None:
    
    print(f"ITERACIÓN | En el nodo: {nodo_actual}")
    
    # 1. Agente toma la decisión LRTA*
    nodo_siguiente, costo_movimiento = lrta_star_decision(nodo_actual, heuristica, GRAFO_COSTOS)
    
    # Si nodo_siguiente es None, es que no hay salida
    if nodo_siguiente is None:
        print(f"  El nodo {nodo_actual} no tiene salidas. Búsqueda fallida.")
        break
        
    # 2. El agente "aprende" (actualiza h(nodo_actual))
    print(f"  * Heurística de {nodo_actual} actualizada a: {heuristica[nodo_actual]}")
    
    # 3. El agente se mueve
    print(f"  * Moviendo a: {nodo_siguiente} (Costo real: {costo_movimiento})")
    
    ruta_tomada.append((nodo_actual, nodo_siguiente))
    costo_real_acumulado += costo_movimiento
    nodo_actual = nodo_siguiente
    
    print(f"  Estado de las heurísticas: {dict(heuristica)}")
    print("-" * 50)

# --- RESULTADOS FINALES ---
if nodo_actual == OBJETIVO:
    print(f"¡OBJETIVO ALCANZADO: {OBJETIVO}!")
    print(f"  Ruta tomada: {' -> '.join(n[0] for n in ruta_tomada) + ' -> ' + OBJETIVO}")
    print(f"  Costo real total: {costo_real_acumulado}")
else:
    print("La búsqueda terminó sin alcanzar el objetivo.")