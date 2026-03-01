import numpy as np

# --- 1. DATOS DE ENTRADA (Probabilidades a Priori y Verosimilitudes) ---

# Hipótesis: Tener la Enfermedad (E) o No Tenerla (¬E)
P_E = 0.01          # P(E) - Probabilidad a Priori de tener la enfermedad (1%)
P_noE = 1.0 - P_E   # P(¬E) - Probabilidad a Priori de NO tener la enfermedad (99%)

# Evidencia: Prueba Positiva (P) o Prueba Negativa (¬P)

# Probabilidades Condicionadas (Verosimilitud)
P_P_dado_E = 0.99   # P(P | E) - Sensibilidad (Tasa de Verdaderos Positivos)
P_P_dado_noE = 0.10 # P(P | ¬E) - Tasa de Falsos Positivos

# --- 2. CÁLCULO DE LA PROBABILIDAD CONDICIONADA (P(E | P)) ---

# A. Numerador (Probabilidad Conjunta No Normalizada)
# P(P | E) * P(E)
numerador = P_P_dado_E * P_E

# B. Cálculo del Término de Normalización P(P)
# Se calcula usando la Ley de Probabilidad Total:
# P(P) = P(P | E) * P(E) + P(P | ¬E) * P(¬E)

P_P_dado_E_por_P_E = P_P_dado_E * P_E
P_P_dado_noE_por_P_noE = P_P_dado_noE * P_noE

# El normalizador P(P) es la suma de todas las formas de obtener una prueba positiva
normalizador_P_P = P_P_dado_E_por_P_E + P_P_dado_noE_por_P_noE

# C. Aplicación de la Regla de Bayes (Probabilidad Condicionada Final)
# P(E | P) = Numerador / Normalizador
P_E_dado_P = numerador / normalizador_P_P


# --- 3. RESULTADOS ---

print("--- Actualización de Creencia usando Bayes ---")
print(f"Probabilidad a Priori P(Enfermedad): {P_E:.4f}")
print(f"Tasa de Falsos Positivos P(Positivo | No Enfermo): {P_P_dado_noE:.4f}")
print("-" * 50)
print(f"Probabilidad No Normalizada P(P, E) (Numerador): {numerador:.4f}")
print(f"Término de Normalización P(P): {normalizador_P_P:.4f}")
print("-" * 50)
print(f"Probabilidad Condicionada Final P(Enfermedad | Positivo): {P_E_dado_P:.4f}")


# Verificación de la Normalización (Probabilidad del estado opuesto)
P_noE_dado_P = P_P_dado_noE_por_P_noE / normalizador_P_P
suma_final = P_E_dado_P + P_noE_dado_P

print(f"\nP(No Enfermedad | Positivo): {P_noE_dado_P:.4f}")
print(f"Suma de las Probabilidades Finales (Debe ser 1.0): {suma_final:.4f}")