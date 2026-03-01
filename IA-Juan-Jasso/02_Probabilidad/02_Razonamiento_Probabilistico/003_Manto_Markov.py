# --- DEFINICIÓN DE LAS TABLAS DE PROBABILIDAD CONDICIONAL (CPT) ---
# ESTA SECCIÓN FALTABA EN EL CÓDIGO QUE ENVIASTE.

# P(Robo)
P_B = {
    'Si': 0.001,  # P(Robo=Si)
    'No': 0.999   # P(Robo=No)
}

# P(Alarma | Robo) - Padres de A
P_A_dado_B = {
    'Si': {           # Si Robo (B='Si')
        'Si': 0.95,   # P(Alarma=Si | Robo=Si)
        'No': 0.05    # P(Alarma=No | Robo=Si)
    },
    'No': {           # Si No Robo (B='No')
        'Si': 0.01,   # P(Alarma=Si | Robo=No)
        'No': 0.99    # P(Alarma=No | Robo=No)
    }
}

# P(JuanLlama | Alarma) - Hijos de A
P_J_dado_A = {
    'Si': {           # Si Alarma (A='Si')
        'Si': 0.90,   # P(JuanLlama=Si | Alarma=Si)
        'No': 0.10    # P(JuanLlama=No | Alarma=Si)
    },
    'No': {           # Si No Alarma (A='No')
        'Si': 0.05,   # P(JuanLlama=Si | Alarma=No)
        'No': 0.95    # P(JuanLlama=No | Alarma=No)
    }
}
# ----------------------------------------------------------------------


def calcular_probabilidad_conjunta(B, A, J):
    """Calcula P(B, A, J) usando la Regla de la Cadena."""
    # Accede a las CPTs definidas arriba
    prob_b = P_B[B]
    prob_a_dado_b = P_A_dado_B[B][A]
    prob_j_dado_a = P_J_dado_A[A][J]
    
    return prob_j_dado_a * prob_a_dado_b * prob_b


def inferir_a_dado_bj(B_evidencia, J_evidencia):
    """Calcula P(A | B, J) usando solo el Manto de Markov {B, J}."""
    
    # Nota: El error de lógica estaba aquí, en la marginalización sobre A, 
    # solo deberías iterar sobre los estados de A, no usar B_evidencia
    estados_A = ['Si', 'No']
    
    # Paso 1: Calcular los términos no normalizados para A='Si' y A='No'
    # P(A=Si, B=Si, J=No)
    prob_A_Si_no_norm = calcular_probabilidad_conjunta(B_evidencia, 'Si', J_evidencia)
    # P(A=No, B=Si, J=No)
    prob_A_No_no_norm = calcular_probabilidad_conjunta(B_evidencia, 'No', J_evidencia)
    
    # Paso 2: Normalización (Cálculo del Denominador P(B, J))
    # P(B, J) = P(A=Si, B, J) + P(A=No, B, J)
    normalizador = prob_A_Si_no_norm + prob_A_No_no_norm
    
    # Paso 3: Probabilidad a Posteriori (Resultado Final)
    P_A_dado_BJ = prob_A_Si_no_norm / normalizador
    
    return P_A_dado_BJ, normalizador

# --- Ejecución del Ejemplo del Manto de Markov ---

Robo_Evi = 'Si'    # Evidencia 1: El Padre de A
Juan_Evi = 'No'    # Evidencia 2: El Hijo de A

prob_A_dado_MB, normalizador_MB = inferir_a_dado_bj(Robo_Evi, Juan_Evi)

print("--- Ilustración del Principio del Manto de Markov ---")
print(f"Buscamos: P(Alarma=Si | Robo={Robo_Evi}, JuanLlama={Juan_Evi})")
print("El Manto de Markov de Alarma (A) es: {Robo, JuanLlama}")
print("-" * 65)

print(f"Probabilidad P(A=Si, B=Si, J=No) [No normalizada]: {calcular_probabilidad_conjunta(Robo_Evi, 'Si', Juan_Evi):.6f}")
print(f"Probabilidad P(A=No, B=Si, J=No) [No normalizada]: {calcular_probabilidad_conjunta(Robo_Evi, 'No', Juan_Evi):.6f}")
print(f"Normalizador P(Robo=Si, JuanLlama=No): {normalizador_MB:.6f}")
print("-" * 65)

print(f"P(Alarma=Si | Manto de Markov = {{Si, No}}): {prob_A_dado_MB:.4f}")
print(f"P(Alarma=No | Manto de Markov = {{Si, No}}): {1.0 - prob_A_dado_MB:.4f}")