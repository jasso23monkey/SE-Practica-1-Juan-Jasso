import random

# CPTs base (las mismas que en ejemplos anteriores)
P_R = 0.2
P_S = 0.1
P_W_dado_RS = {
    ('Si', 'Si'): 0.99, ('Si', 'No'): 0.90,
    ('No', 'Si'): 0.90, ('No', 'No'): 0.01
}
EVIDENCIA_W = 'Si' 

# --- Distribuciones Condicionales Completas (DCC) ---
# Gibbs requiere P(Xi | X_restantes)

# 1. DCC de R: P(R | S, W)
# Calculada usando Bayes: P(R|S,W) = alpha * P(W|R,S) * P(R) * P(S) (si S fuera también fijo)
# P(R|S,W) = alpha * P(W|R,S) * P(R)
def P_R_dado_SW(S, W):
    # Calculamos el numerador no normalizado para R='Si' y R='No'
    num_Si = P_W_dado_RS[('Si', S)] * P_R
    num_No = (1.0 - P_W_dado_RS[('No', S)]) * (1.0 - P_R) # P(W=No|R=No,S)P(R=No) si W fuera 'No'
    
    # Ajuste para W='Si'
    if W == 'Si':
        num_W_Si = P_W_dado_RS[('Si', S)] * P_R 
        num_W_No = P_W_dado_RS[('No', S)] * (1.0 - P_R)
    else: # W == 'No'
        num_W_Si = (1.0 - P_W_dado_RS[('Si', S)]) * P_R
        num_W_No = (1.0 - P_W_dado_RS[('No', S)]) * (1.0 - P_R)

    normalizador = num_W_Si + num_W_No
    return num_W_Si / normalizador if normalizador > 0 else 0.0 # P(R=Si | S, W)

# 2. DCC de S: P(S | R, W)
# P(S|R,W) = alpha * P(W|R,S) * P(S)
def P_S_dado_RW(R, W):
    # Numerador no normalizado para S='Si' y S='No'
    
    # S = Si
    prob_W_dado_RS_Si = P_W_dado_RS[(R, 'Si')]
    num_Si = (prob_W_dado_RS_Si if W == 'Si' else 1.0 - prob_W_dado_RS_Si) * P_S
    
    # S = No
    prob_W_dado_RS_No = P_W_dado_RS[(R, 'No')]
    num_No = (prob_W_dado_RS_No if W == 'Si' else 1.0 - prob_W_dado_RS_No) * (1.0 - P_S)

    normalizador = num_Si + num_No
    return num_Si / normalizador if normalizador > 0 else 0.0 # P(S=Si | R, W)

def muestreo_gibbs(num_iteraciones, burn_in):
    """Implementa el algoritmo de Muestreo de Gibbs."""
    
    # 1. Inicialización de la cadena (Estado aleatorio)
    R = 'Si' if random.random() < P_R else 'No'
    S = 'Si' if random.random() < P_S else 'No'
    
    # Acumulador de resultados
    conteo_R_Si = 0
    
    for t in range(num_iteraciones):
        
        # --- MUESTREO SECUENCIAL DE LA CADENA ---
        
        # A. Muestrear R dado S y W (P(R | S, W))
        # W se fija a la evidencia (EVIDENCIA_W)
        prob_R_Si = P_R_dado_SW(S, EVIDENCIA_W)
        R = 'Si' if random.random() < prob_R_Si else 'No'
        
        # B. Muestrear S dado R y W (P(S | R, W))
        # W se fija a la evidencia (EVIDENCIA_W)
        prob_S_Si = P_S_dado_RW(R, EVIDENCIA_W)
        S = 'Si' if random.random() < prob_S_Si else 'No'
        
        # --- Acumulación (Ignorando el período de calentamiento) ---
        if t >= burn_in:
            if R == 'Si':
                conteo_R_Si += 1
    
    # Inferencia: P(R=Si | W=Si) = Conteo(R=Si) / Total de pasos
    muestras_utilizadas = num_iteraciones - burn_in
    P_R_dado_W_aprox = conteo_R_Si / muestras_utilizadas
    
    return P_R_dado_W_aprox

# --- Ejecución ---
NUM_ITERACIONES = 50000 
BURN_IN = 1000 # Descartar las primeras 1000 muestras

P_R_Gibbs = muestreo_gibbs(NUM_ITERACIONES, BURN_IN)

print("--- Inferencia MCMC: Muestreo de Gibbs ---")
print(f"Evidencia fijada (W): '{EVIDENCIA_W}'")
print(f"Iteraciones totales: {NUM_ITERACIONES}")
print(f"Muestras utilizadas (después de Burn-in): {NUM_ITERACIONES - BURN_IN}")
print("-" * 50)
print(f"Aproximación de P(Lluvia=Sí | Húmedo=Sí): {P_R_Gibbs:.4f}")
print(f"Aproximación de P(Lluvia=No | Húmedo=Sí): {1.0 - P_R_Gibbs:.4f}")