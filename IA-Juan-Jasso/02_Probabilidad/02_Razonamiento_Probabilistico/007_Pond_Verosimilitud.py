import random

# Definición de las probabilidades (CPTs)
P_R = 0.2       # P(Lluvia = Si)
P_S = 0.1       # P(Aspersor = Si)

# P(Césped Húmedo = Si | Lluvia, Aspersor)
P_W_dado_RS = { 
    ('Si', 'Si'): 0.99,
    ('Si', 'No'): 0.90,
    ('No', 'Si'): 0.90,
    ('No', 'No'): 0.01
}

def muestreo_ponderacion_verosimilitud(num_muestras, evidencia):
    """
    Genera muestras para P(R | W=Si) usando Ponderación de Verosimilitud.
    
    evidencia debe ser un diccionario: {'W': 'Si'}
    """
    
    # Acumuladores de pesos
    conteo_R_Si = 0.0  # Suma de pesos donde R = 'Si'
    conteo_R_No = 0.0  # Suma de pesos donde R = 'No'
    
    for _ in range(num_muestras):
        # Inicializar el peso de la muestra
        peso_w = 1.0 
        
        # --- 1. FIJACIÓN y MUESTREO (Orden: R, S, W) ---
        
        # 1. Muestrear R (Lluvia) - No es evidencia
        R = 'Si' if random.random() < P_R else 'No'
        
        # 2. Muestrear S (Aspersor) - No es evidencia
        S = 'Si' if random.random() < P_S else 'No'
        
        # 3. Fijar W (Césped Húmedo) - Es evidencia
        W = evidencia['W']
        
        # --- 2. PONDERACIÓN (Asignar el peso) ---
        # El peso es la probabilidad de la evidencia dado sus padres (R y S)
        
        # Obtener la probabilidad P(W=Evidencia | R, S)
        
        # 3a. Determinar la probabilidad de W=Si dado R y S muestreados
        prob_W_dado_RS = P_W_dado_RS[(R, S)]
        
        if W == 'Si':
            # El peso es P(W=Si | R, S)
            peso_w = prob_W_dado_RS
        else:
            # El peso es P(W=No | R, S)
            peso_w = 1.0 - prob_W_dado_RS
            
        # --- 3. INFERENCIA (Acumular pesos) ---
        if R == 'Si':
            conteo_R_Si += peso_w
        else:
            conteo_R_No += peso_w
            
    # Normalización Final
    suma_total_pesos = conteo_R_Si + conteo_R_No
    
    if suma_total_pesos > 0:
        P_R_Si_dado_W = conteo_R_Si / suma_total_pesos
    else:
        P_R_Si_dado_W = 0.0
        
    return P_R_Si_dado_W, suma_total_pesos

# --- Ejecución ---
EVIDENCIA = {'W': 'Si'}
NUM_MUESTRAS = 100000

P_R_dado_W_lw, suma_pesos = muestreo_ponderacion_verosimilitud(NUM_MUESTRAS, EVIDENCIA)

print("--- Ponderación de Verosimilitud ---")
print(f"Evidencia fijada: Césped Húmedo = '{EVIDENCIA['W']}'")
print(f"Total de muestras generadas: {NUM_MUESTRAS}")
print(f"Suma de todos los pesos (normalizador): {suma_pesos:.4f}")
print("-" * 50)
print(f"Aproximación de P(Lluvia=Sí | Húmedo=Sí): {P_R_dado_W_lw:.4f}")
print(f"Aproximación de P(Lluvia=No | Húmedo=Sí): {1.0 - P_R_dado_W_lw:.4f}")