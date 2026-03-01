import numpy as np

# --- 1. Definición del Modelo Oculto de Markov (HMM) ---

ESTADOS = ['Normal', 'Fallo']
OBSERVACIONES = ['Bajo', 'Medio', 'Alto'] # <-- CORREGIDO
N_ESTADOS = len(ESTADOS)

# A: Matriz de Transición de Estados (Markov) P(Xt | X_{t-1})
A = np.array([
    [0.9, 0.1],  # Desde Normal -> [Normal, Fallo]
    [0.3, 0.7]   # Desde Fallo -> [Normal, Fallo]
])

# B: Matriz de Emisión (Observación) P(Et | Xt)
# Fila: Estado Oculto, Columna: [Bajo, Medio, Alto] <-- CORREGIDO
B = np.array([
    [0.8, 0.15, 0.05],  # En Normal
    [0.05, 0.25, 0.7]   # En Fallo
])

# Pi: Probabilidades Iniciales P(X0)
Pi = np.array([0.5, 0.5]) 

# Mapeo de Observaciones a Índices
obs_map = {'Bajo': 0, 'Medio': 1, 'Alto': 2} # <-- CORREGIDO


# --- 2. Algoritmos de Inferencia (El resto del código de funciones permanece igual) ---

def filtrar_forward(obs_secuencia):
    """
    1. Filtrado: P(Xt | E_{1:t})
    Implementa el Algoritmo Forward.
    """
    T = len(obs_secuencia)
    alpha = np.zeros((T, N_ESTADOS))
    
    # Inicialización (t=0)
    idx_e0 = obs_map[obs_secuencia[0]]
    alpha[0, :] = Pi * B[:, idx_e0] # Pi * P(E0 | X0)
    
    # Recursión (t=1 a T-1)
    for t in range(1, T):
        idx_et = obs_map[obs_secuencia[t]]
        
        prediccion_paso = np.dot(alpha[t-1, :], A)
        
        alpha[t, :] = prediccion_paso * B[:, idx_et]
        
        # Normalización
        alpha[t, :] /= np.sum(alpha[t, :])
        
    return alpha[-1, :]


def predecir(obs_filtrada, k_pasos):
    """
    2. Predicción: P(X_{t+k} | E_{1:t})
    Extiende el resultado filtrado k pasos usando solo la matriz de transición A.
    """
    P_Xt = obs_filtrada 
    
    P_X_futuro = P_Xt
    for _ in range(k_pasos):
        P_X_futuro = np.dot(P_X_futuro, A)
        
    return P_X_futuro


def suavizado_viterbi(obs_secuencia):
    """
    4. Explicación (Decodificación): argmax P(X_{1:t} | E_{1:t})
    Implementa el Algoritmo de Viterbi.
    """
    T = len(obs_secuencia)
    
    delta = np.zeros((T, N_ESTADOS))
    psi = np.zeros((T, N_ESTADOS), dtype=int)
    
    # Inicialización (t=0)
    idx_e0 = obs_map[obs_secuencia[0]]
    delta[0, :] = Pi * B[:, idx_e0]
    
    # Recursión (t=1 a T-1)
    for t in range(1, T):
        idx_et = obs_map[obs_secuencia[t]]
        for j in range(N_ESTADOS): # Estado Futuro
            trans_probs = delta[t-1, :] * A[:, j]
            
            max_prob = np.max(trans_probs)
            max_idx = np.argmax(trans_probs)
            
            delta[t, j] = B[j, idx_et] * max_prob
            psi[t, j] = max_idx

    # Recuperación de la Secuencia más Probable
    secuencia_optima = [0] * T
    secuencia_optima[T-1] = np.argmax(delta[T-1, :])
    
    # Retroceso (Backtracking)
    for t in range(T-2, -1, -1):
        secuencia_optima[t] = psi[t+1, secuencia_optima[t+1]]
    
    secuencia_estados = [ESTADOS[i] for i in secuencia_optima]
    return secuencia_estados

# --- 3. Ejecución y Resultados (Parte que no necesita cambios) ---

OBSERVACIONES_MES = ['Bajo', 'Bajo', 'Bajo', 'Medio', 'Alto', 'Alto', 'Alto', 'Bajo']
OBSERVACIONES_HOY = OBSERVACIONES_MES[:-1] # Observaciones hasta ayer

print("==============================================")
print("             INFERENCIA EN HMM                ")
print("==============================================")

# 1. FILTRADO (Estado actual: el último de la secuencia, 'Alto')
P_filtrado = filtrar_forward(OBSERVACIONES_HOY)
print("\n1. FILTRADO (Prob. Estado HOY): P(X_hoy | E_1:hoy)")
for i, p in enumerate(P_filtrado):
    print(f"   P({ESTADOS[i]} | E_1:hoy): {p:.4f}")


# 2. PREDICCIÓN (Estado futuro: 1 día después de hoy)
PASOS_FUTURO = 1
P_prediccion = predecir(P_filtrado, PASOS_FUTURO)
print(f"\n2. PREDICCIÓN (Prob. Estado FUTURO en +{PASOS_FUTURO} día):")
for i, p in enumerate(P_prediccion):
    print(f"   P({ESTADOS[i]} | E_1:hoy): {p:.4f}")


# 3. SUAVIZADO (Concepto y Algoritmo)
P_filtrado_pasado = filtrar_forward(OBSERVACIONES_HOY[:-2]) # Filtrado hasta anteayer
print("\n3. SUAVIZADO (Estado PASADO: Hace 2 días)")
print(f"   - Filtrado hace 2 días (P(X_-2 | E_1:-2)): {P_filtrado_pasado}")
print("   - **El Suavizado** P(X_-2 | E_1:hoy) usaría la info de hoy para corregir esta estimación.")

# 4. EXPLICACIÓN (Secuencia más probable del pasado)
secuencia_viterbi = suavizado_viterbi(OBSERVACIONES_HOY)
print("\n4. EXPLICACIÓN (Secuencia de estados más probable):")
print(f"   - Observaciones (E_1:ayer): {OBSERVACIONES_HOY}")
print(f"   - Secuencia más probable (Viterbi): {secuencia_viterbi}")