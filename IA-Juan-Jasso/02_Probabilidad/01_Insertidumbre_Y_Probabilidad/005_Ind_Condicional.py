import numpy as np

# --- 1. DEFINICIÓN DE PROBABILIDADES DE ENTRADA ---
P_G = 0.05  # P(Gripe)
P_noG = 1.0 - P_G

# Probabilidades Condicionales de Fiebre (F)
P_F_dado_G = 0.90
P_F_dado_noG = 0.10

# Probabilidades Condicionales de Tos (T)
P_T_dado_G = 0.80
P_T_dado_noG = 0.05

# --- 2. CÁLCULO DE LA PROBABILIDAD CONJUNTA P(F, T, G) ---

# Queremos calcular la probabilidad conjunta de que un paciente al azar:
# Tenga Fiebre (F) AND Tenga Tos (T) AND Tenga Gripe (G)
# P(F, T, G)

# Aplicamos la Regla General de la Cadena:
# P(F, T, G) = P(F | T, G) * P(T | G) * P(G)

# Aquí es donde se aplica la INDEPENDENCIA CONDICIONAL:
# Asumimos que P(F | T, G) = P(F | G)
# Es decir, la Tos no da información extra sobre la Fiebre si ya sabemos de la Gripe.

P_F_T_G = P_F_dado_G * P_T_dado_G * P_G
# P(F, T, G) = 0.90 * 0.80 * 0.05 = 0.036

print("--- Cálculo de Probabilidad Conjunta con Independencia Condicional ---")
print(f"La probabilidad a priori de Gripe P(G) es: {P_G}")
print("Asunción de Independencia Condicional: P(F | T, G) = P(F | G)")
print("-" * 60)
print("P(Fiebre, Tos, Gripe) = P(F | G) * P(T | G) * P(G)")
print(f"P(F, T, G) = {P_F_dado_G} * {P_T_dado_G} * {P_G} = {P_F_T_G:.4f}")
print("-" * 60)


# --- 3. CÁLCULO PARA EL CASO SIN GRIPE (P(F, T, ¬G)) ---

# La independencia condicional también aplica al caso opuesto:
# P(F | T, ¬G) = P(F | ¬G)

P_F_T_noG = P_F_dado_noG * P_T_dado_noG * P_noG
# P(F, T, ¬G) = 0.10 * 0.05 * 0.95 = 0.00475

print(f"P(Fiebre, Tos, NO Gripe) = P(F | ¬G) * P(T | ¬G) * P(¬G)")
print(f"P(F, T, ¬G) = {P_F_dado_noG} * {P_T_dado_noG} * {P_noG} = {P_F_T_noG:.4f}")

# --- 4. CÁLCULO DE P(F | T) (Inferencia Posterior) ---

# Podemos usar los resultados anteriores para calcular P(F | T)
# P(F, T) = P(F, T, G) + P(F, T, ¬G)
P_F_T = P_F_T_G + P_F_T_noG

# P(T) = P(T, G) + P(T, ¬G) -> (Calculamos P(T) para obtener la probabilidad de Tos)
# P(T, G) = P(T | G) * P(G) = 0.80 * 0.05 = 0.04
# P(T, ¬G) = P(T | ¬G) * P(¬G) = 0.05 * 0.95 = 0.0475
P_T = (P_T_dado_G * P_G) + (P_T_dado_noG * P_noG) 
# P_T = 0.04 + 0.0475 = 0.0875

# P(F | T) = P(F, T) / P(T)

P_F_dado_T = P_F_T / P_T

print("-" * 60)
print("INFERENCIA FINAL (Beneficio de la Independencia Condicional):")
print(f"Probabilidad de Fiebre y Tos P(F, T): {P_F_T:.4f}")
print(f"Probabilidad de Tos P(T): {P_T:.4f}")
print(f"Probabilidad Condicionada P(Fiebre | Tos) = P(F, T) / P(T): {P_F_dado_T:.4f}")