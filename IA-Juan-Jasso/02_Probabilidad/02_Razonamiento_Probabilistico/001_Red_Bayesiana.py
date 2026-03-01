# --- 1. Definición de las Tablas de Probabilidad Condicional (CPT) ---

# CPT 1: P(Robo) - Probabilidad A Priori (Nodo Raíz)
P_B = {
    'Si': 0.001,  # P(Robo=Si)
    'No': 0.999   # P(Robo=No)
}

# CPT 2: P(Alarma | Robo) - Probabilidad Condicional
# Estructura: P(Alarma)[Robo]
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

# CPT 3: P(JuanLlama | Alarma) - Probabilidad Condicional
# Estructura: P(JuanLlama)[Alarma]
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

# --- 2. CÁLCULO DE LA PROBABILIDAD CONJUNTA ---

# El corazón de la Red Bayesiana es la factorización:
# P(B, A, J) = P(J | A) * P(A | B) * P(B)

def calcular_probabilidad_conjunta(B, A, J):
    """Calcula la probabilidad P(B, A, J) para un conjunto de valores."""
    
    # 1. P(B) - P(Robo)
    prob_b = P_B[B]
    
    # 2. P(A | B) - P(Alarma dado Robo)
    prob_a_dado_b = P_A_dado_B[B][A]
    
    # 3. P(J | A) - P(JuanLlama dado Alarma)
    prob_j_dado_a = P_J_dado_A[A][J]
    
    # Multiplicación para obtener P(B, A, J)
    return prob_j_dado_a * prob_a_dado_b * prob_b

# Ejemplo: Probabilidad de que Haya Robo, la Alarma Suene y Juan llame.
P_Si_Si_Si = calcular_probabilidad_conjunta('Si', 'Si', 'Si')
# P(B=Si, A=Si, J=Si) = P(J=Si|A=Si) * P(A=Si|B=Si) * P(B=Si)
# P(Si, Si, Si) = 0.90 * 0.95 * 0.001 = 0.000855

print("--- Red Bayesiana (Cálculo Básico Manual) ---")
print(f"P(Robo=Si, Alarma=Si, JuanLlama=Si): {P_Si_Si_Si:.6f}")
print("-" * 45)


# --- 3. INFERENCIA MANUAL (Diagnóstico: P(Robo | JuanLlama=Si)) ---

# Queremos calcular P(B | J=Si). Usaremos la Regla de Bayes y Normalización.
# P(B | J=Si) = P(B, J=Si) / P(J=Si)

# Variables a iterar: Robo (B) y Alarma (A)
estados_B = ['Si', 'No']
estados_A = ['Si', 'No']
evidencia_J = 'Si' # Juan llama

# 3.1. Calcular la probabilidad conjunta NO NORMALIZADA P(B, J=Si) para cada estado de B

# P_B_J_Si representa el numerador no normalizado P(B=b, J=Si) para b={Si, No}
P_B_J_Si = {'Si': 0, 'No': 0} 

for B in estados_B:
    # Marginalización: Sumar sobre todos los posibles estados de A
    # P(B, J=Si) = SUM_A [ P(B, A, J=Si) ]
    suma_sobre_A = 0
    for A in estados_A:
        # Calcular el término P(B, A, J=Si)
        prob_conjunta = calcular_probabilidad_conjunta(B, A, evidencia_J)
        suma_sobre_A += prob_conjunta
        
    P_B_J_Si[B] = suma_sobre_A

# 3.2. Normalización (Cálculo del Denominador P(J=Si))
# P(J=Si) = P(B=Si, J=Si) + P(B=No, J=Si)
normalizador = P_B_J_Si['Si'] + P_B_J_Si['No']

# 3.3. Probabilidad a Posteriori
P_Robo_dado_Juan = P_B_J_Si['Si'] / normalizador
P_NoRobo_dado_Juan = P_B_J_Si['No'] / normalizador


print("Resultado de Inferencia P(Robo | JuanLlama=Si):")
print(f"Probabilidad P(Robo=Si, JuanLlama=Si) [No normalizado]: {P_B_J_Si['Si']:.6f}")
print(f"Probabilidad P(Robo=No, JuanLlama=Si) [No normalizado]: {P_B_J_Si['No']:.6f}")
print(f"Normalizador P(JuanLlama=Si): {normalizador:.6f}")
print(f"P(Robo=Si | JuanLlama=Si) (Posteriori): {P_Robo_dado_Juan:.4f}")
print(f"P(Robo=No | JuanLlama=Si) (Posteriori): {P_NoRobo_dado_Juan:.4f}")
print(f"Suma final (debe ser 1.0): {P_Robo_dado_Juan + P_NoRobo_dado_Juan:.4f}")