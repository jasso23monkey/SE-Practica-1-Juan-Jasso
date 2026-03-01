# Definición de las acciones y sus resultados (Probabilidad, Utilidad)

OPCION_A_SEGURA = [
    (0.3, 50),  # (P(s'|a), U(s')) para Ganancia Grande
    (0.6, 20),  # (P(s'|a), U(s')) para Ganancia Media
    (0.1, 0)    # (P(s'|a), U(s')) para Pérdida Leve
]

OPCION_B_ARRIESGADA = [
    (0.1, 100), # (P(s'|a), U(s')) para Ganancia Enorme
    (0.9, -5)   # (P(s'|a), U(s')) para Pérdida Fuerte
]

def calcular_utilidad_esperada(opcion):
    """Calcula la utilidad esperada (EU) para una lista de resultados (probabilidad, utilidad)."""
    utilidad_esperada = 0
    for probabilidad, utilidad in opcion:
        # EU = Suma de [Probabilidad * Utilidad]
        utilidad_esperada += probabilidad * utilidad
    return utilidad_esperada

# --- Ejecución ---

eu_a = calcular_utilidad_esperada(OPCION_A_SEGURA)
eu_b = calcular_utilidad_esperada(OPCION_B_ARRIESGADA)

print("--- Análisis de Utilidad ---")
print(f"Utilidad Esperada (Opción A Segura): {eu_a:.2f}")
print(f"Utilidad Esperada (Opción B Arriesgada): {eu_b:.2f}")

print("\n--- Decisión del Agente (MEU) ---")

if eu_a > eu_b:
    decision = "Opción A (Segura)"
    mejor_utilidad = eu_a
elif eu_b > eu_a:
    decision = "Opción B (Arriesgada)"
    mejor_utilidad = eu_b
else:
    decision = "Indiferente, cualquier opción."
    mejor_utilidad = eu_a

print(f"El agente, buscando maximizar la Utilidad Esperada, elige la: {decision}")
print(f"Utilidad Máxima Esperada (MEU): {mejor_utilidad:.2f}")