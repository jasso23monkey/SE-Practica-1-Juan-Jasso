import numpy as np

# Reglas Simuladas de una LPCFG: P(FV | Cabeza de FN)
# Muestra cómo la probabilidad de usar el verbo "mira" o "miran"
# depende del sustantivo ("perro" vs "perros").

LPCFG_REGLAS_FV = {
    # 1. Sustantivo singular (HEAD='perro')
    'perro': {
        'FV -> V(mira)': 0.95,  # Es muy probable que el verbo sea singular
        'FV -> V(miran)': 0.05   # Es improbable que el verbo sea plural
    },
    # 2. Sustantivo plural (HEAD='perros')
    'perros': {
        'FV -> V(mira)': 0.10,  # Es improbable que el verbo sea singular
        'FV -> V(miran)': 0.90   # Es muy probable que el verbo sea plural
    }
}

# Probabilidades de las reglas léxicas (simplificadas)
REGLAS_LEXICAS = {
    'N': {'perro': 0.6, 'perros': 0.4},
    'V': {'mira': 0.5, 'miran': 0.5}
}

def calcular_probabilidad_frase(sustantivo_cabeza, verbo_elegido):
    """
    Calcula la probabilidad de una estructura FN(h) FV(v)
    usando la regla condicional de la cabeza.
    """
    
    # Paso 1: Probabilidad de la regla de concordancia FV
    # P(FV -> V(v) | N(h))
    try:
        regla_fv_prob = LPCFG_REGLAS_FV[sustantivo_cabeza][f'FV -> V({verbo_elegido})']
    except KeyError:
        return 0.0 # Caso de regla no definida

    # Paso 2: Probabilidad de la regla léxica del sustantivo
    # P(N -> h)
    prob_sustantivo = REGLAS_LEXICAS['N'][sustantivo_cabeza]
    
    # Paso 3: Probabilidad de la regla léxica del verbo
    # P(V -> v)
    prob_verbo = REGLAS_LEXICAS['V'][verbo_elegido]
    
    # Probabilidad total de esta parte de la estructura
    # P(Estructura) = P(FV|N) * P(N) * P(V)
    probabilidad_total = regla_fv_prob * prob_sustantivo * prob_verbo
    
    return probabilidad_total

# --- 3. Ejecución y Comparación ---

print("=====================================================")
print("  SIMULACIÓN LPCFG: CONCORDANCIA Y PROBABILIDAD      ")
print("=====================================================")

# A. Frase Gramaticalmente Correcta (Singular - Alta Probabilidad)
# Estructura: FN(perro) FV(mira)
prob_A = calcular_probabilidad_frase('perro', 'mira')
print(f"1. P(FV(mira) | N(perro)): {LPCFG_REGLAS_FV['perro']['FV -> V(mira)']:<5} (Regla de concordancia)")
print(f"   P(\"perro mira\"): {prob_A:.6f}")
print("-" * 50)


# B. Frase Gramaticalmente Incorrecta (Singular + Plural - Baja Probabilidad)
# Estructura: FN(perro) FV(miran)
prob_B = calcular_probabilidad_frase('perro', 'miran')
print(f"2. P(FV(miran) | N(perro)): {LPCFG_REGLAS_FV['perro']['FV -> V(miran)']:<5} (Regla de discordancia)")
print(f"   P(\"perro miran\"): {prob_B:.6f}")
print("-" * 50)


# C. Frase Gramaticalmente Correcta (Plural - Alta Probabilidad)
# Estructura: FN(perros) FV(miran)
prob_C = calcular_probabilidad_frase('perros', 'miran')
print(f"3. P(FV(miran) | N(perros)): {LPCFG_REGLAS_FV['perros']['FV -> V(miran)']:<5} (Regla de concordancia)")
print(f"   P(\"perros miran\"): {prob_C:.6f}")
print("-" * 50)

# 4. Conclusión LPCFG
print("CONCLUSIÓN:")
print(f"La LPCFG asigna una probabilidad mucho mayor a las frases con concordancia:")
print(f"P(\"perro mira\") ≈ {prob_A:.6f} vs P(\"perro miran\") ≈ {prob_B:.6f}")

