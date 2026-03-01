import numpy as np

# --- 1. Definición del HMM para el Reconocimiento del Habla ---

# Los "estados" son los fonemas de las palabras "Toma" y "Loma".
ESTADOS_HMM = ['T/L', 'o', 'm', 'a'] 
N_ESTADOS = len(ESTADOS_HMM)

# Las "observaciones" son las características acústicas.
OBSERVACIONES = ['Fuerte', 'Suave']
obs_map = {'Fuerte': 0, 'Suave': 1}

# --- 2. Parámetros del Modelo de Lenguaje (Decodificación) ---

# PI: Probabilidades Iniciales P(X0) para los 4 estados.
# CORRECCIÓN CLAVE: El vector debe tener tamaño N_ESTADOS=4.
# Se asume que el proceso SIEMPRE comienza en el primer fonema ('T/L').
PI = np.array([1.0, 0.0, 0.0, 0.0]) # [P(T/L), P(o), P(m), P(a)]

# Matriz de Transición (A): P(Fonema_t | Fonema_{t-1})
# Transición obligatoria hacia el siguiente fonema.
A = np.array([
    [0.0, 1.0, 0.0, 0.0],  # De T/L solo puede ir a 'o'
    [0.0, 0.0, 1.0, 0.0],  # De 'o' solo puede ir a 'm'
    [0.0, 0.0, 0.0, 1.0],  # De 'm' solo puede ir a 'a'
    [0.0, 0.0, 0.0, 0.0]   # Fin
])

# --- 3. Parámetros del Modelo Acústico (Emisión) ---

# B: Matriz de Emisión P(Observación | Estado Oculto)
# Fila: Fonema Oculto (T/L, o, m, a) ; Columna: [Fuerte, Suave]
B = np.array([
    [0.8, 0.2],  # T/L: Más Fuerte -> 'Toma'; Más Suave -> 'Loma'
    [0.5, 0.5],  # 'o': Neutro
    [0.4, 0.6],  # 'm': Tiende a ser 'Suave'
    [0.3, 0.7]   # 'a': Tiende a ser 'Suave'
])

# --- 4. Algoritmo de Viterbi para Decodificación de Habla ---

def viterbi_decodificacion_simple(observaciones, A, B, PI):
    """Implementación del Algoritmo de Viterbi."""
    T = len(observaciones)
    
    delta = np.zeros((T, N_ESTADOS))
    psi = np.zeros((T, N_ESTADOS), dtype=int)
    
    # Inicialización (t=0)
    idx_e0 = obs_map[observaciones[0]]
    # delta[0, :] ahora es (4,) * (4,), lo cual es compatible.
    delta[0, :] = PI * B[:, idx_e0] 
    
    # Recursión (t=1 a T-1)
    for t in range(1, T):
        idx_et = obs_map[observaciones[t]]
        
        for j in range(N_ESTADOS): # Estado Futuro
            trans_probs = delta[t-1, :] * A[:, j]
            
            max_prob = np.max(trans_probs)
            max_idx = np.argmax(trans_probs)
            
            delta[t, j] = B[j, idx_et] * max_prob
            psi[t, j] = max_idx

    # Recuperación de la Secuencia Óptima
    secuencia_optima = [0] * T
    secuencia_optima[T-1] = np.argmax(delta[T-1, :])
    
    # Retroceso (Backtracking)
    for t in range(T - 2, -1, -1):
        secuencia_optima[t] = psi[t+1, secuencia_optima[t+1]]
    
    secuencia_fonemas = [ESTADOS_HMM[i] for i in secuencia_optima]
    
    # La decisión final se basa en el primer fonema decodificado.
    if secuencia_fonemas[0] == 'T/L':
         # Comprobamos si el camino de mayor probabilidad corresponde a la T o L
         # Se usa una simplificación ya que el modelo solo tiene 4 estados y una palabra.
         # En un modelo real, habría caminos separados para T-o-m-a y L-o-m-a.
         # Aquí, interpretamos T/L como T si la probabilidad total del camino T fue mayor.
         prob_toma = delta[-1, 0] # La prob final del camino "T" (solo si es el estado final)
         prob_loma = delta[-1, 0] # La prob final del camino "L"
         
         # Para nuestro modelo simplificado, si la primera observación fue 'Fuerte', asumimos T, si fue 'Suave', asumimos L
         if observaciones[0] == 'Fuerte':
             palabra_decodificada = "Toma"
         else:
             palabra_decodificada = "Loma"
    else:
        # Esto no debería ocurrir si el modelo de transición es correcto
        palabra_decodificada = "ERROR: No inicio en T/L"
        
    return palabra_decodificada, np.max(delta[T-1, :])


# --- 5. Prueba de Decodificación ---

# Caso 1: La observación es 'Suave' al inicio (tiende a ser 'Loma')
AUDIO_CASO_1 = ['Suave', 'Suave', 'Suave', 'Suave'] 

# Caso 2: La observación es 'Fuerte' al inicio (tiende a ser 'Toma')
AUDIO_CASO_2 = ['Fuerte', 'Suave', 'Suave', 'Suave']

palabra_1, prob_1 = viterbi_decodificacion_simple(AUDIO_CASO_1, A, B, PI)
palabra_2, prob_2 = viterbi_decodificacion_simple(AUDIO_CASO_2, A, B, PI)

print("--- Decodificación de Habla Simulada (Toma vs. Loma) ---")
print(f"Observación 1: {AUDIO_CASO_1}")
print(f"Decodificación más probable: '{palabra_1}' (Prob: {prob_1:.6e})")
print("-" * 30)
print(f"Observación 2: {AUDIO_CASO_2}")
print(f"Decodificación más probable: '{palabra_2}' (Prob: {prob_2:.6e})")