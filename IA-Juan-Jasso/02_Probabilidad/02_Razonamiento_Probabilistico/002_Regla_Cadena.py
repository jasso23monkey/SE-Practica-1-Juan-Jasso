# --- 1. Definición de las Probabilidades Condicionales (Las "Tablas") ---

# P(Robo)
P_B = 0.001

# P(Alarma | Robo)
# [P(A=Si | B=Si), P(A=Si | B=No)]
P_A_dado_B = {
    'Si': 0.95,  # P(Alarma=Si | Robo=Si)
    'No': 0.01   # P(Alarma=Si | Robo=No)
}

# P(JuanLlama | Alarma)
# [P(J=Si | A=Si), P(J=Si | A=No)]
P_J_dado_A = {
    'Si': 0.90,  # P(JuanLlama=Si | Alarma=Si)
    'No': 0.05   # P(JuanLlama=Si | Alarma=No)
}

# --- 2. APLICACIÓN DE LA REGLA DE LA CADENA ---

# Definimos los valores específicos para el cálculo:
Robo = 'Si'
Alarma = 'No'
JuanLlama = 'Si'

# 1. P(B)
prob_b = P_B

# 2. P(A | B)
# Probabilidad de que la alarma suene DADO que hay robo.
prob_a_dado_b = P_A_dado_B[Robo]

# 3. P(J | A)
# Probabilidad de que Juan llame DADO que la alarma suena.
prob_j_dado_a = P_J_dado_A[Alarma]

# Multiplicación en cadena: P(B, A, J) = P(J | A) * P(A | B) * P(B)
probabilidad_conjunta = prob_j_dado_a * prob_a_dado_b * prob_b


# --- 3. RESULTADOS ---

print("--- Cálculo con la Regla de la Cadena ---")
print(f"Buscamos la Probabilidad Conjunta P(Robo={Robo}, Alarma={Alarma}, JuanLlama={JuanLlama})")
print("-" * 65)
print(f"P(B): {prob_b:.5f}")
print(f"P(A | B): {prob_a_dado_b:.5f}")
print(f"P(J | A): {prob_j_dado_a:.5f}")
print("-" * 65)

print("P(B, A, J) = P(J | A) * P(A | B) * P(B)")
print(f"P(B, A, J) = {prob_j_dado_a:.5f} * {prob_a_dado_b:.5f} * {prob_b:.5f}")
print(f"Resultado de la Probabilidad Conjunta: {probabilidad_conjunta:.7f}")
