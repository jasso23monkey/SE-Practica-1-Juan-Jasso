# Definición de un Proceso de Decisión de Markov (MDP)

# --- 1. COMPONENTES DEL MDP ---

ESTADOS = ['S0', 'S1', 'S2', 'S3']
ACCIONES = ['N', 'E']
GAMMA = 0.9 

RECOMPENSA = {'S0': 0, 'S1': 0, 'S2': 0, 'S3': 10} 

# Probabilidad de Transición: P(s' | s, a)
# La clave de este ejemplo es la incertidumbre.
P_EXITO = 0.8  # Probabilidad de ir a donde se pretende
P_FALLO = 0.2  # Probabilidad de 'deslizarse' (perpendicular)

# Definición simplificada de las Transiciones (sin contemplar todos los bordes para brevedad)
# TRANSICIONES[s][a] = {s_destino_principal: P, s_deslizamiento_1: P, ...}
TRANSICIONES = {
    'S0': {
        'E': {'S1': P_EXITO, 'S2': P_FALLO},  # Intenta E (S1), puede deslizarse a N (S2)
        'N': {'S2': P_EXITO, 'S1': P_FALLO}   # Intenta N (S2), puede deslizarse a E (S1)
    },
    'S1': {
        'E': {'S1': 1.0}, # Borde, se queda en S1
        'N': {'S3': P_EXITO, 'S1': P_FALLO} 
    },
    'S2': {
        'E': {'S3': P_EXITO, 'S0': P_FALLO}, # Intenta E (S3), puede deslizarse a O (S0)
        'N': {'S2': 1.0}  # Borde, se queda en S2
    },
    'S3': {
        'E': {'S3': 1.0},
        'N': {'S3': 1.0}
    }
}

# --- 2. POLÍTICA FIJA PARA EVALUAR ---
# π(s) = acción. El agente siempre intenta ir al Este (E) donde pueda.
POLITICA_FIJA = {'S0': 'E', 'S1': 'E', 'S2': 'E', 'S3': 'E'}


# --- 3. EVALUACIÓN DE LA POLÍTICA V^π (Policy Evaluation) ---

def evaluar_politica_un_paso(V_actual):
    """Calcula V^(pi)_{k+1}(s) para todos los estados basado en V_k."""
    V_siguiente = V_actual.copy()
    
    for s in ESTADOS:
        if s == 'S3':
            V_siguiente[s] = RECOMPENSA['S3'] # El valor de la meta es fijo (10)
            continue
            
        a = POLITICA_FIJA[s] # Acción determinada por la política fija
        
        # Ecuación de Bellman para Evaluación de Políticas:
        # V^pi(s) = R(s, pi(s)) + gamma * Sum_{s'} P(s'|s, pi(s)) * V^pi(s')
        
        suma_valor_futuro = 0
        
        # Transición: P(s'|s, a)
        for s_prime, p_transicion in TRANSICIONES[s][a].items():
            
            # Suma de P(s'|s, a) * V^pi(s')
            suma_valor_futuro += p_transicion * V_actual[s_prime]
            
        # Cálculo final del nuevo valor del estado V_siguiente
        r_s_a = RECOMPENSA[s] # Recompensa inmediata (es 0 en S0, S1, S2)
        V_siguiente[s] = r_s_a + GAMMA * suma_valor_futuro
        
    return V_siguiente

# --- 4. SIMULACIÓN Y CONVERGENCIA ---

V = {s: 0.0 for s in ESTADOS} # V0 inicializado a cero
NUM_ITERACIONES = 10

print(f"--- Evaluando Política π (siempre 'E') en un MDP con P(éxito)={P_EXITO} ---")

for i in range(1, NUM_ITERACIONES + 1):
    V = evaluar_politica_un_paso(V)
    
    # Imprimir la propagación del valor
    valores = [f'{s}={V[s]:.3f}' for s in ESTADOS]
    print(f"Iteración {i:02d}: {', '.join(valores)}")

print("\n" + "="*50)
print("VALOR FINAL V^π(s) de la política 'E':")
print(V)