# --- 1. Definición de las CPTs (Probabilidades) ---

# P(Robo)
P_B = {'Si': 0.001, 'No': 0.999}

# P(Alarma | Robo)
P_A_dado_B = {
    'Si': {'Si': 0.95, 'No': 0.05},  # P(A | B=Si)
    'No': {'Si': 0.01, 'No': 0.99}   # P(A | B=No)
}

# P(JuanLlama | Alarma)
P_J_dado_A = {
    'Si': {'Si': 0.90, 'No': 0.10},  # P(J | A=Si)
    'No': {'Si': 0.05, 'No': 0.95}   # P(J | A=No)
}

# --- FUNCIÓN BASE: Cálculo de la Probabilidad Conjunta ---

def calcular_probabilidad_conjunta(B, A, J):
    """P(B, A, J) = P(J | A) * P(A | B) * P(B)"""
    return P_J_dado_A[A][J] * P_A_dado_B[B][A] * P_B[B]

# --- 2. INFERENCIA POR ENUMERACIÓN ---

def inferencia_por_enumeracion(query, evidence_value):
    """Calcula P(Robo | JuanLlama=Si) usando enumeración sobre A (Alarma)."""
    
    estados_B = ['Si', 'No']
    estados_A = ['Si', 'No']
    
    # Almacenará los términos no normalizados P(B, J=Si)
    P_B_dado_J_no_norm = {'Si': 0.0, 'No': 0.0}
    
    # 1. ENUMERACIÓN (Marginalización sobre A)
    for B in estados_B:
        suma_sobre_A = 0.0
        for A in estados_A:
            prob_conjunta_termino = calcular_probabilidad_conjunta(B, A, evidence_value)
            suma_sobre_A += prob_conjunta_termino
            
        P_B_dado_J_no_norm[B] = suma_sobre_A

    # 2. NORMALIZACIÓN
    normalizador = P_B_dado_J_no_norm['Si'] + P_B_dado_J_no_norm['No']
    
    # 3. RESULTADO (Probabilidad a Posteriori)
    P_B_Si_post = P_B_dado_J_no_norm['Si'] / normalizador
    P_B_No_post = P_B_dado_J_no_norm['No'] / normalizador
    
    # Devuelve el valor NO normalizado también para el print final
    return P_B_Si_post, P_B_No_post, normalizador, P_B_dado_J_no_norm['Si']

# --- 3. EJECUCIÓN ---

# Pregunta: ¿Cuál es la probabilidad de Robo si Juan llama?
prob_si_robo, prob_no_robo, normalizador, P_B_Si_J_no_norm = inferencia_por_enumeracion('Robo', 'Si')

print("--- Inferencia por Enumeración (P(Robo | Juan llama=Si)) ---")
print("Variable Oculta enumerada (SUM): Alarma (A)")
print("-" * 70)

# Usamos la variable no normalizada que ahora es retornada por la función
print(f"Probabilidad P(Robo=Si, JuanLlama=Si) [No normalizada]: {P_B_Si_J_no_norm:.6f}")
print(f"Normalizador P(JuanLlama=Si): {normalizador:.6f}")
print("-" * 70)
print(f"P(Robo=Si | JuanLlama=Si) (Posteriori): {prob_si_robo:.4f}")
print(f"P(Robo=No | JuanLlama=Si) (Posteriori): {prob_no_robo:.4f}")
print(f"Suma final (debe ser 1.0): {prob_si_robo + prob_no_robo:.4f}")