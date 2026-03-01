#import numpy as np

# --- 1. DATOS DE ENTRADA (Probabilidades A Priori y Verosimilitudes) ---

# Hipótesis: Defectuoso (D) o No Defectuoso (¬D)
P_D = 0.01          # P(D) - Probabilidad a Priori de que un producto sea defectuoso (1%)
P_noD = 1.0 - P_D   # P(¬D) - Probabilidad a Priori de que NO sea defectuoso (99%)

# Evidencia: Detector Positivo (Pos)

# Probabilidad Condicionada (Verosimilitud): Detector reacciona si hay Defecto
P_Pos_dado_D = 0.95   # P(Pos | D) - Tasa de Verdaderos Positivos (95%)
# Probabilidad Condicionada: Detector reacciona si NO hay Defecto
P_Pos_dado_noD = 0.05 # P(Pos | ¬D) - Tasa de Falsos Positivos (5%)


# --- 2. CÁLCULO BAYESIANO ---

# A. Numerador (Probabilidad Conjunta No Normalizada)
# P(Pos | D) * P(D)
numerador = P_Pos_dado_D * P_D

# B. Cálculo del Término de Normalización P(Pos) (Ley de Probabilidad Total)
# P(Pos) = P(Pos | D) * P(D) + P(Pos | ¬D) * P(¬D)

P_Pos_dado_D_por_P_D = P_Pos_dado_D * P_D       # Verdaderos Positivos
P_Pos_dado_noD_por_P_noD = P_Pos_dado_noD * P_noD # Falsos Positivos

# El normalizador P(Pos) es la suma de las dos vías de obtener una alarma
normalizador_P_Pos = P_Pos_dado_D_por_P_D + P_Pos_dado_noD_por_P_noD

# C. Probabilidad a Posteriori (Regla de Bayes)
# P(D | Pos) = Numerador / Normalizador
P_D_dado_Pos = numerador / normalizador_P_Pos


# --- 3. RESULTADOS ---

print("--- Evaluación Bayesiana de la Alarma de un Detector ---")
print(f"Probabilidad a Priori P(Defectuoso): {P_D:.4f}")
print(f"Falsos Positivos P(Positivo | No Defectuoso): {P_Pos_dado_noD:.4f}")
print("-" * 60)

print(f"Probabilidad No Normalizada P(Positivo y Defectuoso): {numerador:.4f}")
print(f"Término de Normalización P(Positivo Total): {normalizador_P_Pos:.4f}")
print("-" * 60)

print(f"Probabilidad a Posteriori P(Defectuoso | Positivo): {P_D_dado_Pos:.4f}")

# Verificación de la Normalización (P(¬D | Pos))
P_noD_dado_Pos = P_Pos_dado_noD_por_P_noD / normalizador_P_Pos
suma_final = P_D_dado_Pos + P_noD_dado_Pos

print(f"\nProbabilidad de NO ser Defectuoso | Positivo: {P_noD_dado_Pos:.4f}")
print(f"Suma de las Probabilidades Finales (Debe ser 1.0): {suma_final:.4f}")