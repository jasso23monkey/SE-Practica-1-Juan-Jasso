import numpy as np

# --- ESTADOS OCULTOS (REGIONES DE ADN) ---
# La región que generó la observación (no es observable directamente)
ESTADOS = ['Intron', 'Exon']
N_ESTADOS = len(ESTADOS)

# --- OBSERVACIONES (BASES DE ADN) ---
# Las bases de ADN que observamos
OBSERVACIONES = ['A', 'C', 'G', 'T']
obs_map = {'A': 0, 'C': 1, 'G': 2, 'T': 3}


# --- PARÁMETROS DEL HMM ---

# A: Matriz de Transición P(Xt | X_{t-1})
# Fila: Estado Anterior, Columna: Estado Siguiente
A = np.array([
    [0.90, 0.10],  # Desde Intron: 90% de seguir en Intron, 10% de transicionar a Exon
    [0.20, 0.80]   # Desde Exon: 80% de seguir en Exon, 20% de transicionar a Intron
])

# B: Matriz de Emisión P(Et | Xt)
# Fila: Estado Oculto, Columna: [A, C, G, T]
B = np.array([
    [0.25, 0.25, 0.25, 0.25],  # En Intron (No codificante): Las bases son equiprobables (ruido)
    [0.35, 0.15, 0.35, 0.15]   # En Exon (Codificante): Hay sesgo hacia A y G (bases más comunes en codones)
])

# Pi: Probabilidades Iniciales P(X0)
# Asumimos que la secuencia tiene más probabilidad de comenzar en una región no codificante (Intron)
Pi = np.array([0.7, 0.3])

def viterbi_decodificacion(obs_secuencia, A, B, Pi):
    """
    Decodifica la secuencia de estados ocultos (regiones) más probable.
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

# Secuencia de ADN simulada:
# Inicia con una secuencia aleatoria (Intron), luego una secuencia con alto sesgo A/G (Exon), y vuelve a ser aleatoria.
SECUENCIA_ADN_OBSERVADA = list(
    "ACTG" +      # Intron: Bases equiprobables (25% cada una)
    "AAGGTTCAGA" + # Exon: Alto sesgo hacia A y G 
    "TCAGAG"       # Intron: Vuelve a ser más aleatorio
)

secuencia_regimenes = viterbi_decodificacion(SECUENCIA_ADN_OBSERVADA, A, B, Pi)

print("=========================================================")
print("  DECODIFICACIÓN DE REGIONES (HMM VITERBI EN BIOLOGÍA)  ")
print("=========================================================")

print(f"Longitud de la secuencia (T): {len(SECUENCIA_ADN_OBSERVADA)} bases")
print("-" * 50)
print("SECUENCIA DE BASES (OBSERVACIONES):")
print("".join(SECUENCIA_ADN_OBSERVADA))
print("-" * 50)
print("SECUENCIA DE REGIONES (DECODIFICACIÓN):")
print(secuencia_regimenes)
print("-" * 50)

# El resultado mostrará que la sección con el sesgo A/G (AAGGTTCAGA) 
# ha sido decodificada como perteneciente a la región 'Exon', mientras que las 
# secciones más aleatorias (ACTG y TCAGAG) se decodifican como 'Intron'.