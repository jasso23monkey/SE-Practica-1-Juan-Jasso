import numpy as np

# --- 1. Definición del Modelo Oculto de Markov (HMM) ---

ESTADOS = ['Normal', 'Fallo']
N_ESTADOS = len(ESTADOS)

# A: Matriz de Transición P(Xt | X_{t-1})
A = np.array([
    [0.9, 0.1],  # Normal -> [Normal, Fallo]
    [0.3, 0.7]   # Fallo  -> [Normal, Fallo]
])

# B: Matriz de Emisión P(Et | Xt)
# Columna: [Bajo, Medio, Alto]
B = np.array([
    [0.8, 0.15, 0.05],  # En estado Normal
    [0.05, 0.25, 0.7]   # En estado Fallo
])

# Pi: Probabilidades Iniciales P(X0)
Pi = np.array([0.5, 0.5]) 

# Mapeo de Observaciones a Índices
obs_map = {'Bajo': 0, 'Medio': 1, 'Alto': 2}


# Secuencia de Observaciones (E_1:T) a lo largo de 5 días (T=5)
OBSERVACIONES_EVIDENCIA = ['Bajo', 'Bajo', 'Medio', 'Alto', 'Alto']
T = len(OBSERVACIONES_EVIDENCIA)


# -----------------------------------------------------------------
## FUNCIÓN 1: PASO HACIA DELANTE (FORWARD PASS)
# -----------------------------------------------------------------

def forward_pass(obs_secuencia, A, B, Pi):
    """Calcula la probabilidad delantera (alpha_t)."""
    T = len(obs_secuencia)
    alpha = np.zeros((T, N_ESTADOS))
    
    # 1. Inicialización (t=0)
    idx_e0 = obs_map[obs_secuencia[0]]
    alpha[0, :] = Pi * B[:, idx_e0]
    
    # Normalización del primer paso (opcional, pero buena práctica)
    alpha[0, :] /= np.sum(alpha[0, :])
    
    # 2. Recursión (t=1 a T-1)
    for t in range(1, T):
        idx_et = obs_map[obs_secuencia[t]]
        
        # P(Xt | X_{t-1}) * alpha_{t-1}
        prediccion_paso = np.dot(alpha[t-1, :], A)
        
        # alpha_t = P(Et | Xt) * prediccion_paso
        alpha[t, :] = prediccion_paso * B[:, idx_et]
        
        # Normalización
        alpha[t, :] /= np.sum(alpha[t, :])
        
    return alpha

# -----------------------------------------------------------------
## FUNCIÓN 2: PASO HACIA ATRÁS (BACKWARD PASS)
# -----------------------------------------------------------------

def backward_pass(obs_secuencia, A, B):
    """Calcula la probabilidad trasera (beta_t)."""
    T = len(obs_secuencia)
    beta = np.zeros((T, N_ESTADOS))
    
    # 1. Inicialización (t=T-1)
    # beta[T-1, i] = 1 (por convención)
    beta[T-1, :] = 1.0
    
    # 2. Recursión (t=T-2 hasta t=0, hacia atrás)
    for t in range(T - 2, -1, -1):
        idx_et1 = obs_map[obs_secuencia[t+1]] # Evidencia E_{t+1}
        
        for i in range(N_ESTADOS): # Estado actual (Xi)
            
            # P(X_{t+1} | Xi) * P(E_{t+1} | X_{t+1}) * beta_{t+1}
            suma_transicion = A[i, :] * B[:, idx_et1] * beta[t+1, :]
            
            # beta_t(i) = SUM_{X_{t+1}} [suma_transicion]
            beta[t, i] = np.sum(suma_transicion)
            
        # Normalización (para evitar underflow, al igual que en alpha)
        beta[t, :] /= np.sum(beta[t, :])
        
    return beta

# -----------------------------------------------------------------
## FUNCIÓN 3: ALGORITMO COMPLETO (SUAVIZADO)
# -----------------------------------------------------------------

def forward_backward_smoothing(alpha, beta, k):
    """
    Combina alpha y beta para calcular la probabilidad suavizada P(Xk | E_{1:T})
    para el tiempo 'k'.
    """
    # 1. Combinación (gamma_k = alpha_k * beta_k)
    # El vector gamma en el tiempo k es el producto elemento a elemento
    gamma_k = alpha[k, :] * beta[k, :]
    
    # 2. Normalización
    P_suavizado = gamma_k / np.sum(gamma_k)
    
    return P_suavizado


# -----------------------------------------------------------------
## EJECUCIÓN DEL ALGORITMO Y RESULTADOS
# -----------------------------------------------------------------

# Paso 1: Ejecutar el Forward Pass
alpha_matrix = forward_pass(OBSERVACIONES_EVIDENCIA, A, B, Pi)

# Paso 2: Ejecutar el Backward Pass
beta_matrix = backward_pass(OBSERVACIONES_EVIDENCIA, A, B)

# Tiempo de interés para el suavizado (k=2 es el Día 3, cuando se observó 'Medio')
K_TIME = 2 

# Paso 3: Calcular el Suavizado
P_suavizado_k = forward_backward_smoothing(alpha_matrix, beta_matrix, K_TIME)
P_filtrado_k = alpha_matrix[K_TIME] # El filtrado en el tiempo K solo usa evidencia hasta K

print("=========================================================")
print("      ALGORITMO HACIA DELANTE-ATRÁS (SUAVIZADO)          ")
print("=========================================================")

print(f"Secuencia de Observaciones (E_1:T): {OBSERVACIONES_EVIDENCIA}")
print(f"Tiempo de Suavizado (k): Día {K_TIME + 1} (Observación: '{OBSERVACIONES_EVIDENCIA[K_TIME]}')")

print("\n--- Resultados en el Día k (Día 3) ---")

# Filtrado (solo usa E_1:k)
print("1. Probabilidad Filtrada (P(X_k | E_1:k)):")
for i, p in enumerate(P_filtrado_k):
    print(f"   - P(X_3 = {ESTADOS[i]}): {p:.4f}")

# Suavizado (usa E_1:T)
print("\n2. Probabilidad Suavizada (P(X_k | E_1:T)):")
for i, p in enumerate(P_suavizado_k):
    print(f"   - P(X_3 = {ESTADOS[i]}): {p:.4f}")
    
print("\n--- Conclusión ---")
# Comparación
print("El estado 'Fallo' en el Día 3 era: ")
print(f"   - Filtrado: {P_filtrado_k[1]:.4f}")
print(f"   - Suavizado: {P_suavizado_k[1]:.4f}")
print("El valor suavizado utiliza la evidencia posterior ('Alto', 'Alto') para corregir la estimación del pasado.")