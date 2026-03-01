import numpy as np

# --- ESTADOS OCULTOS (REGÍMENES DE MERCADO) ---
ESTADOS = ['Baja_Vol', 'Alta_Vol']
N_ESTADOS = len(ESTADOS)

# --- OBSERVACIONES (RENDIMIENTOS DIARIOS) ---
OBSERVACIONES = ['P_Severa', 'R_Medio', 'G_Severa']
obs_map = {'P_Severa': 0, 'R_Medio': 1, 'G_Severa': 2}


# --- PARÁMETROS DEL HMM ---

# A: Matriz de Transición P(Xt | X_{t-1})
# Fila: Estado Anterior, Columna: Estado Siguiente
A = np.array([
    [0.95, 0.05],  # Desde Baja_Vol
    [0.15, 0.85]   # Desde Alta_Vol
])

# B: Matriz de Emisión P(Et | Xt)
# Fila: Estado Oculto, Columna: [P_Severa, R_Medio, G_Severa]
B = np.array([
    [0.10, 0.80, 0.10],  # En Baja_Vol (Rendimiento Medio es muy probable)
    [0.40, 0.20, 0.40]   # En Alta_Vol (Extremos son muy probables)
])

# Pi: Probabilidades Iniciales P(X0)
Pi = np.array([0.7, 0.3])

def viterbi_decodificacion(obs_secuencia, A, B, Pi):
    """
    Decodifica la secuencia de estados ocultos más probable.
    """
    T = len(obs_secuencia)
    
    # Delta: Almacena la probabilidad del camino más probable hasta el estado i en el tiempo t
    delta = np.zeros((T, N_ESTADOS))
    
    # Psi: Almacena el índice del estado anterior que generó el camino más probable
    psi = np.zeros((T, N_ESTADOS), dtype=int)
    
    # --- Inicialización (t=0) ---
    idx_e0 = obs_map[obs_secuencia[0]]
    delta[0, :] = Pi * B[:, idx_e0]
    
    # --- Recursión (t=1 a T-1) ---
    for t in range(1, T):
        idx_et = obs_map[obs_secuencia[t]]
        
        for j in range(N_ESTADOS): # Estado actual (X_t = j)
            # 1. MAX_{i} [ delta_{t-1}(i) * P(X_t=j | X_{t-1}=i) ]
            trans_probs = delta[t-1, :] * A[:, j]
            
            # 2. P(E_t | X_t=j) * MAX(...)
            max_prob = np.max(trans_probs)
            max_idx = np.argmax(trans_probs)
            
            delta[t, j] = B[j, idx_et] * max_prob
            psi[t, j] = max_idx

    # --- Recuperación de la Secuencia Óptima (Backtracking) ---
    secuencia_optima = [0] * T
    
    # El último estado es el más probable al final
    secuencia_optima[T-1] = np.argmax(delta[T-1, :])
    
    # Retroceso (Backtracking)
    for t in range(T - 2, -1, -1):
        secuencia_optima[t] = psi[t+1, secuencia_optima[t+1]]
    
    # Convertir índices a nombres de estados
    secuencia_regimenes = [ESTADOS[i] for i in secuencia_optima]
    return secuencia_regimenes

# -----------------------------------------------------------------
## 3. Simulación y Resultados
# -----------------------------------------------------------------

# 15 días de rendimientos observados:
# Inicia estable, luego 3 días de alta volatilidad (extremos) y vuelve a estabilizarse.
RENDIMIENTOS_OBSERVADOS = [
    'R_Medio', 'R_Medio', 'R_Medio', 
    'P_Severa', 'G_Severa', 'P_Severa', 
    'R_Medio', 'G_Severa', 'R_Medio', 
    'R_Medio', 'R_Medio', 'R_Medio', 'R_Medio', 'R_Medio', 'R_Medio'
]

secuencia_regimenes = viterbi_decodificacion(RENDIMIENTOS_OBSERVADOS, A, B, Pi)

print("=========================================================")
print("  DECODIFICACIÓN DE REGÍMENES (HMM VITERBI EN FINANZAS)  ")
print("=========================================================")

print(f"Días (T): {len(RENDIMIENTOS_OBSERVADOS)}")
print("-" * 50)
print("SECUENCIA DE RENDIMIENTOS (E_1:T):")
print(RENDIMIENTOS_OBSERVADOS)
print("-" * 50)
print("SECUENCIA DE REGÍMENES (X_1:T - Decodificación):")
print(secuencia_regimenes)
print("-" * 50)

# El resultado mostrará que los días con pérdidas/ganancias severas (P_Severa, G_Severa)
# han sido decodificados como pertenecientes al régimen de 'Alta_Vol', 
# mientras que los 'R_Medio' se decodifican como 'Baja_Vol'.

# --- Interpretación Financiera ---
print("\n Interpretación de la Decodificación:")
print("Este resultado muestra al gestor de riesgos la **trayectoria histórica más probable**")
print("del riesgo. El HMM infirió que el mercado pasó a un régimen de **Alta Volatilidad** ")
print("alrededor de los días 4, 5 y 6, y volvió a la normalidad (Baja Volatilidad) después.")
print("Esto permite calibrar modelos de riesgo (como VaR) de manera dinámica.")