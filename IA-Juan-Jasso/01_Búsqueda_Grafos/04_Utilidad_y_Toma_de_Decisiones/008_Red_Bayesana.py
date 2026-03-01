import numpy as np

# --- 1. DEFINICIÓN DE LA RBD (Modelo Oculto de Markov) ---

ESTADOS = ['Limpio', 'Sucio']
OBSERVACIONES = ['OK', 'RUIDO']

# Mapeo para facilitar el acceso a arrays
S_MAP = {'Limpio': 0, 'Sucio': 1}
O_MAP = {'OK': 0, 'RUIDO': 1}

# A. Distribución Inicial P(Z0)
# P(Z0=Limpio)=0.8, P(Z0=Sucio)=0.2
prob_inicial = np.array([0.8, 0.2])

# B. Probabilidad de Transición P(Z_t+1 | Z_t)
# Fila = Z_t (Estado Anterior); Columna = Z_t+1 (Estado Siguiente)
# |       | Limpio | Sucio |
# | L (0) | 0.7    | 0.3   |
# | S (1) | 0.1    | 0.9   |
prob_transicion = np.array([
    [0.7, 0.3],
    [0.1, 0.9]
])

# C. Probabilidad de Emisión (Observación) P(E_t | Z_t)
# Fila = Z_t (Estado Oculto); Columna = E_t (Observación)
# |       | OK (0) | RUIDO (1) |
# | L (0) | 0.9    | 0.1       |
# | S (1) | 0.2    | 0.8       |
prob_emision = np.array([
    [0.9, 0.1],
    [0.2, 0.8]
])

# --- 2. SECUENCIA DE OBSERVACIONES ---

# El agente ve tres lecturas ruidosas, luego una lectura OK.
secuencia_observaciones = ['RUIDO', 'RUIDO', 'RUIDO', 'OK']

# --- 3. ALGORITMO DE FILTRADO (Forward Pass) ---

def filtrar_estado(secuencia_obs):
    """
    Implementa el Algoritmo de Avance (Forward) para calcular la distribución
    de probabilidad sobre el estado actual P(Z_t | E_1:t)
    """
    b_actual = prob_inicial.copy() # b_0 = P(Z_0)
    
    historial_creencias = [b_actual]
    
    print(f"Paso 0 (Inicial): {ESTADOS[0]}={b_actual[0]:.4f}, {ESTADOS[1]}={b_actual[1]:.4f}")

    for t, obs in enumerate(secuencia_obs):
        obs_idx = O_MAP[obs]
        b_siguiente_sin_norm = np.zeros(len(ESTADOS))
        
        # 1. PREDICCIÓN (Paso Temporal): P(Z_{t+1} | E_{1:t})
        # Se usa b_actual y la matriz de Transición
        b_predict = np.dot(b_actual, prob_transicion)
        
        # 2. ACTUALIZACIÓN (Paso de Observación): P(Z_{t+1} | E_{t+1}, E_{1:t})
        # Se incorpora la observación E_{t+1} usando la matriz de Emisión
        
        normalizador = 0
        for s_prime_idx in range(len(ESTADOS)):
            # P(E | Z') * P(Z')
            p_emision_s_prime = prob_emision[s_prime_idx, obs_idx]
            b_siguiente_sin_norm[s_prime_idx] = p_emision_s_prime * b_predict[s_prime_idx]
            normalizador += b_siguiente_sin_norm[s_prime_idx]
            
        # Normalización
        b_siguiente = b_siguiente_sin_norm / normalizador
        
        # Preparar para la siguiente iteración
        b_actual = b_siguiente
        historial_creencias.append(b_actual)
        
        print(f"Paso {t+1} (Obs='{obs}'): {ESTADOS[0]}={b_actual[0]:.4f}, {ESTADOS[1]}={b_actual[1]:.4f}")
        
    return b_actual

# Ejecución del Filtrado
print("--- Inferencia de Filtrado en RBD (Robot Limpiador) ---")
creencia_final = filtrar_estado(secuencia_observaciones)