import numpy as np

# Reglas de Producción y sus Probabilidades
# La suma de las probabilidades para cada No Terminal (lado izquierdo) debe ser 1.0
PCFG_RULES = {
    # 1. Sentencia (S) - Debe empezar en S
    'S': [
        ('FN FV', 1.0)
    ],
    # 2. Frase Nominal (FN)
    'FN': [
        ('Det N', 0.8),    # Ej: "el perro"
        ('FN PP', 0.2)     # Ej: "el perro en el parque"
    ],
    # 3. Frase Verbal (FV)
    'FV': [
        ('V FN', 0.7),     # Ej: "mira la pelota"
        ('FV PP', 0.3)     # Ej: "mira la pelota con el telescopio"
    ],
    # 4. Frase Preposicional (PP)
    'PP': [
        ('P FN', 1.0)      # Ej: "con el telescopio"
    ],
    # Reglas Terminales (Léxico)
    'Det': [('el', 0.5), ('la', 0.5)],
    'N':   [('perro', 0.3), ('pelota', 0.3), ('telescopio', 0.4)],
    'V':   [('mira', 1.0)],
    'P':   [('con', 1.0)]
}

# La frase a analizar
frase = "el perro mira la pelota"

def calcular_probabilidad_arbol(reglas_aplicadas):
    """
    Calcula la probabilidad total de una estructura sintáctica
    multiplicando las probabilidades de todas las reglas usadas.
    """
    probabilidad_total = 1.0
    
    for no_terminal, produccion, probabilidad in reglas_aplicadas:
        probabilidad_total *= probabilidad
    
    return probabilidad_total

# Definición de las reglas usadas para generar la frase "el perro mira la pelota"
REGLAS_ARBOL_SIMPLE = [
    # Reglas Sintácticas
    ('S', 'FN FV', 1.0),      # P(S -> FN FV) = 1.0
    ('FN', 'Det N', 0.8),     # P(FN -> Det N) = 0.8
    ('FV', 'V FN', 0.7),      # P(FV -> V FN) = 0.7
    ('FN', 'Det N', 0.8),     # P(FN -> Det N) = 0.8 (para "la pelota")
    
    # Reglas Léxicas
    ('Det', 'el', 0.5),       # P(Det -> el) = 0.5
    ('N', 'perro', 0.3),      # P(N -> perro) = 0.3
    ('V', 'mira', 1.0),       # P(V -> mira) = 1.0
    ('Det', 'la', 0.5),       # P(Det -> la) = 0.5
    ('N', 'pelota', 0.3)      # P(N -> pelota) = 0.3
]

prob_simple = calcular_probabilidad_arbol(REGLAS_ARBOL_SIMPLE)

print("==================================================")
print("     PCFG: CÁLCULO DE PROBABILIDAD DE ANÁLISIS    ")
print("==================================================")
print(f"Frase a analizar: \"{frase}\"")
print("-" * 50)
print("Probabilidad del Árbol Sintáctico Simple:")
print("Probabilidad Total = 1.0 * 0.8 * 0.7 * 0.8 * 0.5 * 0.3 * 1.0 * 0.5 * 0.3")
print(f"P(Árbol Simple) = {prob_simple:.8f}")

# Definición de reglas para un Árbol 2 (Imaginario y más complejo/largo)
REGLAS_ARBOL_COMPLEJO = [
    # 1. S -> FN FV (1.0)
    ('S', 'FN FV', 1.0),
    
    # 2. FV -> FV PP (0.3) <--- La regla de baja probabilidad
    ('FV', 'FV PP', 0.3),
    
    # 3. FN -> Det N (0.8) (para "el telescopio")
    ('FN', 'Det N', 0.8),
    
    # 4. PP -> P FN (1.0)
    ('PP', 'P FN', 1.0),
    
    # 5. FN -> FN PP (0.2) <--- La otra regla de baja probabilidad
    ('FN', 'FN PP', 0.2),
    
    # ... + reglas léxicas (Digamos que P_lex = 0.005)
    
    ('Léxico', 'Terminación', 0.005) 
]

# Calculamos la probabilidad del árbol complejo
prob_compleja = calcular_probabilidad_arbol(REGLAS_ARBOL_COMPLEJO)

print("\nSimulación de Ambigüedad:")
print("Si tuviéramos un Árbol 2 (más complejo, usando reglas de baja prob):")
print("P(Árbol Complejo, basado en 1.0 * 0.3 * 0.8 * 1.0 * 0.2 * 0.005... ):")
print(f"P(Árbol Complejo) = {prob_compleja:.8f}")
print("-" * 50)

# Conclusión de la PCFG
if prob_simple > prob_compleja:
    print(f"CONCLUSIÓN PCFG: El analizador elige el Árbol Simple ({prob_simple:.8f}),")
    print("ya que es la estructura sintáctica más probable para la frase.")

