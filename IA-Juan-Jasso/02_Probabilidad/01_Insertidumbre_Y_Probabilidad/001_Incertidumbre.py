import numpy as np
import random

# --- 1. CONFIGURACIÓN DEL DILEMA Y PARÁMETROS ---

NUM_BRAZOS = 3
PROBABILIDADES_REALES = [0.4, 0.6, 0.5] # Brazo 1 es el óptimo
PASOS = 500

# Parámetros del Agente
ALPHA = 0.1 # Tasa de aprendizaje
Q_INICIAL = 5.0 # OPTIMISMO: Inicializar Q-values muy altos

# Tablas de Conocimiento del Agente
Q_estimado = np.full(NUM_BRAZOS, Q_INICIAL) # Inicializa la creencia optimista
N_conteo = np.zeros(NUM_BRAZOS)             # Conteo de veces que se jaló cada brazo

# --- 2. FUNCIONES CLAVE ---

def jalar_brazo(brazo_id):
    """Simula jalar el brazo y devuelve la recompensa (0 o 1)."""
    return 1 if random.random() < PROBABILIDADES_REALES[brazo_id] else 0

def elegir_accion_greedy():
    """Elige el brazo con el Q-Value MÁS ALTO (pura explotación)."""
    # La EXPLORACIÓN se fuerza por la sobrestimación de Q_estimado.
    return np.argmax(Q_estimado)

def actualizar_Q(brazo_id, recompensa):
    """Actualiza la estimación Q(a) usando una media incremental (promedio móvil)."""
    N_conteo[brazo_id] += 1
    
    # Media Incremental: Q_nuevo = Q_antiguo + (1/N) * (Recompensa - Q_antiguo)
    n = N_conteo[brazo_id]
    error = recompensa - Q_estimado[brazo_id]
    
    # Nota: Usaremos ALPHA en lugar de (1/n) para un aprendizaje más estable, típico de RL
    Q_estimado[brazo_id] += ALPHA * error

# --- 3. BUCLE PRINCIPAL DE INTERACCIÓN ---

print(f"--- Incertidumbre como Optimismo Inicial (Q0 = {Q_INICIAL}) ---")
print(f"Q Inicial: {Q_estimado}")

for paso in range(PASOS):
    
    # 1. Decisión del agente (solo explotación)
    brazo_elegido = elegir_accion_greedy()
        
    # 2. Interacción y Recompensa
    recompensa = jalar_brazo(brazo_elegido)
    
    # 3. Aprendizaje
    actualizar_Q(brazo_elegido, recompensa)

# --- 4. RESULTADOS Y ANÁLISIS ---

print("-" * 55)
print(f"Total de Pasos: {PASOS}")
print("\nConocimiento final del Agente (Q-Estimado):")

print(f"Q Final: {Q_estimado}")
print("-" * 55)

print("\nAnálisis de Exploración Forzada:")
for i in range(NUM_BRAZOS):
    print(f"  Brazo {i}: Recompensa Estimada (Q) = {Q_estimado[i]:.4f} | Jalado {int(N_conteo[i])} veces")