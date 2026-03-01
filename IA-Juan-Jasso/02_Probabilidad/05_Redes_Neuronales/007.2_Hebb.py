import numpy as np

# --- 1. Configuración Inicial ---
PESO_WAB = 0.1             # Peso inicial entre Neurona A y Neurona B
TASA_APRENDIZAJE = 0.5     # Factor de ajuste (eta)

# Escenarios de activación: [Neurona A, Neurona B]
ESCENARIOS = [
    (1, 1), # Ambas activas (Refuerzo esperado)
    (1, 0), # A activa, B inactiva (Sin cambio o Debilitamiento)
    (0, 1), # A inactiva, B activa (Sin cambio o Debilitamiento)
    (1, 1), # Ambas activas de nuevo (Refuerzo adicional)
]

print("=============================================")
print("          REGLA DE HEBB (APRENDIZAJE)        ")
print("=============================================")
print(f"Peso Inicial W_AB: {PESO_WAB:.2f}")
print("-" * 50)

# --- 2. Bucle de Aprendizaje Hebbiano ---
for i, (activacion_a, activacion_b) in enumerate(ESCENARIOS):
    
    # Regla de Hebb: Delta W_AB = Tasa * Activación_A * Activación_B
    cambio_w = TASA_APRENDIZAJE * activacion_a * activacion_b
    
    # Actualización: W_nuevo = W_antiguo + Delta W
    PESO_WAB += cambio_w
    
    print(f"Paso {i+1}: A={activacion_a}, B={activacion_b}")
    print(f"   Cambio (Delta W): {cambio_w:.2f}")
    print(f"   Peso W_AB Final: {PESO_WAB:.2f}")

print("-" * 50)
print("Conclusión:")
print("El peso solo aumenta cuando las activaciones A y B son 1 (activas).")