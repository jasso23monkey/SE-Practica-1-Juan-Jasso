import numpy as np

# --- 1. DEFINICIÓN DEL MDP ---
ESTADOS = ['S0', 'S1', 'S2', 'S3']
ACCIONES = ['N', 'S', 'E', 'O']
GAMMA = 0.09  # Factor de descuento
RECOMPENSA = {'S0': 0, 'S1': 0, 'S2': 0, 'S3': 10} 
THETA = 0.0001 # Umbral de convergencia para la Evaluación de Política

# Transiciones deterministas (S3 es terminal/absorbente)
TRANSICIONES = {
    'S0': {'N': 'S2', 'E': 'S1', 'S': 'S0', 'O': 'S0'},
    'S1': {'N': 'S3', 'E': 'S1', 'S': 'S1', 'O': 'S0'},
    'S2': {'N': 'S2', 'E': 'S3', 'S': 'S0', 'O': 'S2'},
    'S3': {'N': 'S3', 'E': 'S3', 'S': 'S3', 'O': 'S3'} 
}

# --- 2. FASE 1: EVALUACIÓN DE LA POLÍTICA ---

def evaluar_politica(politica, V):
    """
    Evalúa V^pi(s) para una política dada.
    Usa un ciclo repetido para resolver las ecuaciones de Bellman (iterative policy evaluation).
    """
    while True:
        delta = 0
        V_new = V.copy()
        
        for s in ESTADOS:
            if s == 'S3':
                continue # El valor de la meta es fijo
                
            v_old = V[s]
            a = politica[s] # La acción está fijada por la política pi
            
            s_prime = TRANSICIONES[s][a]
            r_s_a = RECOMPENSA[s]
            
            # V^pi(s) = R(s, pi(s)) + gamma * V^pi(s')
            v_new_s = r_s_a + GAMMA * V[s_prime]
            V_new[s] = v_new_s
            
            delta = max(delta, abs(v_old - v_new_s))
            
        V = V_new
        if delta < THETA:
            break
            
    return V

# --- 3. FASE 2: MEJORA DE LA POLÍTICA ---

def mejorar_politica(V):
    """
    Crea una nueva política pi' que es codiciosa con respecto a V.
    """
    politica_estable = True
    nueva_politica = {}
    
    for s in ESTADOS:
        if s == 'S3':
            nueva_politica[s] = 'TERMINAL'
            continue
            
        antigua_accion = politica_actual[s]
        mejor_q = -np.inf
        mejor_accion = None
        
        # Calcular los Q-valores para todas las acciones posibles
        for a in ACCIONES:
            s_prime = TRANSICIONES[s][a]
            r_s_a = RECOMPENSA[s]
            q_value = r_s_a + GAMMA * V[s_prime]
            
            if q_value > mejor_q:
                mejor_q = q_value
                mejor_accion = a
                
        nueva_politica[s] = mejor_accion
        
        # Comprobar si la política ha cambiado
        if nueva_politica[s] != antigua_accion:
            politica_estable = False
            
    return nueva_politica, politica_estable

# --- 4. ALGORITMO PRINCIPAL DE ITERACIÓN DE POLÍTICAS ---

# Inicialización: Política inicial arbitraria (ej. ir al Este en todas partes)
politica_actual = {'S0': 'E', 'S1': 'E', 'S2': 'E', 'S3': 'TERMINAL'}
V = {s: 0.0 for s in ESTADOS}
politica_estable = False
iteracion_global = 0

print("--- Ejecución de la Iteración de Políticas ---")

while not politica_estable:
    iteracion_global += 1
    print(f"\nITERACIÓN {iteracion_global}:")
    
    # 1. EVALUACIÓN DE LA POLÍTICA
    V = evaluar_politica(politica_actual, V)
    print(f"  V^pi evaluado. Valores V(s): {', '.join([f'{s}={V[s]:.3f}' for s in ESTADOS])}")

    # 2. MEJORA DE LA POLÍTICA
    politica_siguiente, politica_estable = mejorar_politica(V)
    
    print(f"  Política anterior: {politica_actual}")
    print(f"  Política mejorada: {politica_siguiente}")
    
    if not politica_estable:
        politica_actual = politica_siguiente

# --- Resultado Final ---
print("\n" + "="*50)
print(f"CONVERGENCIA LOGRADA en {iteracion_global} iteraciones globales.")
print("\nPOLÍTICA ÓPTIMA π*(s):")
print(politica_actual)
print("\nFUNCIÓN DE VALOR ÓPTIMA V*(s):")
print(V)