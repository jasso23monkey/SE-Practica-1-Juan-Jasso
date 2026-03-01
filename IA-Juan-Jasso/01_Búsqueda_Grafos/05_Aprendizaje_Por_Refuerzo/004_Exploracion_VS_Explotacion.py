import numpy as np
import random

# --- 1. CONFIGURACIÓN DEL DILEMA Y PARÁMETROS ---

# Valores Reales (Ocultos) de los brazos
NUM_BRAZOS = 3
PROBABILIDADES_REALES = [0.4, 0.6, 0.5] # Brazo 1 es el óptimo (60%)

# Parámetros del Agente
EPSILON = 0.5  # Tasa de Exploración (10% de exploración)
PASOS = 1000   # Número total de veces que el agente jala un brazo

# Tablas de Conocimiento del Agente (Lo que el agente APRENDE)
Q_estimado = np.zeros(NUM_BRAZOS)    # Q(a): Recompensa promedio estimada de cada brazo
N_conteo = np.zeros(NUM_BRAZOS)      # N(a): Número de veces que se ha jalado cada brazo

# --- 2. FUNCIONES CLAVE ---

def jalar_brazo(brazo_id):
    """Simula jalar el brazo y devuelve la recompensa (0 o 1)."""
    if random.random() < PROBABILIDADES_REALES[brazo_id]:
        return 1  # Recompensa
    return 0  # Sin recompensa

def elegir_accion(epsilon):
    """Elige el brazo según la estrategia epsilon-greedy."""
    if random.random() < epsilon:
        # 1. EXPLORACIÓN: Elegir un brazo al azar (con probabilidad epsilon)
        return random.choice(range(NUM_BRAZOS))
    else:
        # 2. EXPLOTACIÓN: Elegir el brazo con el Q-Value más alto (con prob. 1-epsilon)
        return np.argmax(Q_estimado)

def actualizar_Q(brazo_id, recompensa):
    """Actualiza las estimaciones de Q(a) y N(a) con la media incremental."""
    
    # 1. Aumentar el contador de veces que se jaló el brazo
    N_conteo[brazo_id] += 1
    
    # 2. Calcular el nuevo promedio de recompensa (Actualización de Q)
    n = N_conteo[brazo_id]
    q_antiguo = Q_estimado[brazo_id]
    
    # Nueva estimación Q = Q_antiguo + (1/N) * (Recompensa - Q_antiguo)
    Q_estimado[brazo_id] = q_antiguo + (1 / n) * (recompensa - q_antiguo)

# --- 3. BUCLE PRINCIPAL DE INTERACCIÓN ---

recompensas_totales = 0
explotacion_conteo = 0
exploracion_conteo = 0

print(f"--- Simulación del Dilema con ε={EPSILON} ---")

for paso in range(PASOS):
    
    # Decisión del agente (Exploración o Explotación)
    brazo_elegido = elegir_accion(EPSILON)
    
    # Clasificar la decisión para el análisis
    if random.random() < EPSILON:
        exploracion_conteo += 1
    else:
        explotacion_conteo += 1
        
    # Interacción con el entorno
    recompensa = jalar_brazo(brazo_elegido)
    
    # Aprendizaje
    actualizar_Q(brazo_elegido, recompensa)
    
    recompensas_totales += recompensa
    
# --- 4. RESULTADOS Y ANÁLISIS ---

print(f"\nNúmero total de pasos: {PASOS}")
print("-" * 35)
print(f"Total de Recompensas Obtenidas: {recompensas_totales}")
print(f"Recompensa Promedio por Paso: {recompensas_totales / PASOS:.4f}")
print(f"Exploración: {exploracion_conteo} veces, Explotación: {explotacion_conteo} veces")
print("-" * 35)

print("\nConocimiento final del Agente (Q-Estimado):")
for i in range(NUM_BRAZOS):
    print(f"  Brazo {i}: Recompensa Estimada (Q) = {Q_estimado[i]:.4f} (Jalado {int(N_conteo[i])} veces)")

print("\nConclusión:")
brazo_ganador = np.argmax(Q_estimado)
if brazo_ganador == 1:
    print(f" ¡El agente identificó correctamente el Brazo {brazo_ganador} (el óptimo)!")
else:
    print(" El agente no pudo identificar el brazo óptimo (el Brazo 1).")