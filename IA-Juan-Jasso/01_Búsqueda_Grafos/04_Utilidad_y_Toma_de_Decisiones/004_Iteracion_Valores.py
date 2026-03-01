import numpy as np

# --- 1. DEFINICIÓN DEL MDP ---

ESTADOS = ['S0', 'S1', 'S2', 'S3']
ACCIONES = ['N', 'S', 'E', 'O']
GAMMA = 0.9  # Factor de descuento
EPSILON = 0.001 # Criterio de parada

# Recompensas R(s): Solo la meta (S3) tiene recompensa
RECOMPENSA = {'S0': 0, 'S1': 0, 'S2': 0, 'S3': 10} 

# Transiciones T(s, a) -> s' (Simplificadas a deterministas)
# P(s' | s, a) = 1 si la transición es posible, 0 en otro caso.
TRANSICIONES = {
    'S0': {'N': 'S2', 'E': 'S1', 'S': 'S0', 'O': 'S0'},
    'S1': {'N': 'S3', 'E': 'S1', 'S': 'S1', 'O': 'S0'},
    'S2': {'N': 'S2', 'E': 'S3', 'S': 'S0', 'O': 'S2'},
    'S3': {'N': 'S3', 'E': 'S3', 'S': 'S3', 'O': 'S3'} # Estado terminal/absorbente
}

# Inicializar la función de valor V(s) a cero
V = {s: 0.0 for s in ESTADOS}
indice_mapa = {s: i for i, s in enumerate(ESTADOS)}

# --- 2. ALGORITMO DE ITERACIÓN DE VALORES ---

def value_iteration():
    global V
    iteracion = 0
    
    print("--- Inicialización: V(s) = 0 para todos los estados. ---")
    
    while True:
        delta = 0  # Máxima diferencia entre V_k y V_{k+1}
        V_new = V.copy()
        iteracion += 1
        
        for s in ESTADOS:
            v_old = V[s]
            
            # El valor del estado terminal es fijo (su recompensa)
            if s == 'S3': 
                V_new[s] = RECOMPENSA['S3']
                continue

            # Calcular el nuevo valor V_{k+1}(s)
            # V_{k+1}(s) = max_a [ R(s, a) + gamma * Sum_{s'} P(s'|s, a) * V_k(s') ]
            
            valores_accion = []
            
            for a in ACCIONES:
                s_prime = TRANSICIONES[s][a]
                r_s_a = RECOMPENSA[s] # R es 0 excepto en la meta S3
                
                # P(s' | s, a) * V_k(s')
                # (Aquí P=1 ya que es determinista)
                valor_futuro = 1.0 * V[s_prime] 
                
                # Se utiliza la recompensa del estado siguiente si fuera diferente de 0.
                # Como solo S3 tiene recompensa, R(s, a) = 0. 
                # La recompensa de la meta se obtiene al llegar a s' = S3. 
                
                q_value = r_s_a + GAMMA * valor_futuro
                valores_accion.append(q_value)
                
            # Actualización de Bellman: tomar el valor máximo (V_{k+1}(s))
            if valores_accion:
                V_new[s] = max(valores_accion)
            
            # Calcular el cambio para el criterio de parada
            delta = max(delta, abs(v_old - V_new[s]))
            
        V = V_new
        
        # Mostrar el progreso de la convergencia
        if iteracion % 1 == 0:
            print(f"Iteración {iteracion:02d}: {', '.join([f'{s}={V[s]:.3f}' for s in ESTADOS])}, Delta={delta:.4f}")

        # Criterio de parada: Convergencia
        if delta < EPSILON * (1 - GAMMA) / GAMMA:
            break
            
    return V, iteracion

# --- 3. EXTRACCIÓN DE LA POLÍTICA ÓPTIMA ---

def extraer_politica_optima(V):
    politica = {}
    for s in ESTADOS:
        if s == 'S3':
            politica[s] = 'TERMINAL'
            continue
            
        mejor_q = -np.inf
        mejor_accion = None
        
        for a in ACCIONES:
            s_prime = TRANSICIONES[s][a]
            r_s_a = RECOMPENSA[s]
            
            q_value = r_s_a + GAMMA * V[s_prime]
            
            if q_value > mejor_q:
                mejor_q = q_value
                mejor_accion = a
        
        politica[s] = mejor_accion
    return politica

# Ejecución del Algoritmo
V_optimo, num_iteraciones = value_iteration()
politica_optima = extraer_politica_optima(V_optimo)

print("\n" + "="*50)
print(f"CONVERGENCIA LOGRADA en {num_iteraciones} iteraciones.")
print("\nFUNCIÓN DE VALOR ÓPTIMA V*(s):")
print(V_optimo)
print("\nPOLÍTICA ÓPTIMA π*(s):")
print(politica_optima)