import numpy as np
import random

# --- 1. CONFIGURACIÓN DEL MDP Y PARÁMETROS ---

# 4 filas x 12 columnas. (0,0) es abajo-izquierda.
FILAS, COLS = 4, 12
START = (0, 0)
GOAL = (0, 11)

# El Acantilado está en Fila 0, Columnas 1 a 10.
CLIFF = [(0, c) for c in range(1, 11)]

# Parámetros de Q-Learning
GAMMA = 0.9
ALPHA = 0.1
EPSILON = 0.1 # Tasa de exploración
EPISODIOS = 10000

ACCIONES = ['N', 'S', 'E', 'O']
Q = {} # Q-Table

# Inicialización de la Q-Table
for r in range(FILAS):
    for c in range(COLS):
        estado = (r, c)
        Q[estado] = {a: 0.0 for a in ACCIONES}

# --- 2. FUNCIONES DE TRANSICIÓN Y RECOMPENSA ---

def get_next_state(s, a):
    """Calcula el siguiente estado y la recompensa. Movimiento determinista."""
    r, c = s
    
    # 1. Calcular el movimiento (s') sin restricciones
    if a == 'N': s_prime = (r + 1, c)
    elif a == 'S': s_prime = (r - 1, c)
    elif a == 'E': s_prime = (r, c + 1)
    else: s_prime = (r, c - 1)
        
    r_prime = -1 # Recompensa por paso

    # 2. Aplicar restricciones y recompensas especiales
    r_prime = -1 # Recompensa por paso
    
    # Restricción: No salirse de la cuadrícula
    if s_prime[0] < 0 or s_prime[0] >= FILAS or s_prime[1] < 0 or s_prime[1] >= COLS:
        s_prime = s # Si choca con la pared, se queda en el mismo estado

    # Restricción: Caer al acantilado
    if s_prime in CLIFF:
        r_prime = -100
        s_prime = START # Vuelve al inicio
        
    return s_prime, r_prime

def choose_action(s):
    """Política epsilon-greedy."""
    if random.random() < EPSILON:
        return random.choice(ACCIONES)
    else:
        q_values = Q[s]
        # Elegir la acción con el Q-Value máximo (Explotación)
        return max(q_values, key=q_values.get)

# --- 3. ALGORITMO PRINCIPAL DE Q-LEARNING ---

for episodio in range(EPISODIOS):
    s = START
    
    while s != GOAL:
        
        # 1. Seleccionar la acción a usar (Política de comportamiento: epsilon-greedy)
        a = choose_action(s)
        
        # 2. Transición
        s_prime, r = get_next_state(s, a)
        
        # 3. Obtener el valor para la actualización (Política objetivo: Max)
        if s_prime == GOAL:
            max_q_prime = 0.0 # Estado terminal/meta
        else:
            max_q_prime = max(Q[s_prime].values()) # max_a' Q(s', a')
            
        # 4. Actualización Q-Learning
        
        # Objetivo TD: r + gamma * max_a' Q(s', a')
        objetivo_td = r + GAMMA * max_q_prime
        
        # Actualización: Q(s, a) <- Q(s, a) + alpha * [Objetivo - Q(s, a)]
        Q[s][a] += ALPHA * (objetivo_td - Q[s][a])
        
        s = s_prime
        
# --- 4. EXTRACCIÓN DE LA POLÍTICA ÓPTIMA ---

def extraer_ruta_y_politica(Q):
    """Extrae la mejor política y una ruta de ejemplo."""
    s = START
    ruta = [START]
    politica = {}
    
    while s != GOAL and s not in CLIFF and len(ruta) < 200: # Límite de seguridad
        a = max(Q[s], key=Q[s].get)
        politica[s] = a
        s, _ = get_next_state(s, a)
        ruta.append(s)
        
    return politica, ruta

# --- 5. RESULTADOS FINALES ---

politica_optima, ruta_ejemplo = extraer_ruta_y_politica(Q)

print("--- APRENDIZAJE ACTIVO: Q-LEARNING EN ACANTILADO ---")
print(f"Episodios: {EPISODIOS}, Exploración (ε): {EPSILON}")

print("\n Política Óptima (π*):")
# Mostrar solo los pasos clave de la ruta
for s in ruta_ejemplo[:10] + ['...'] + ruta_ejemplo[-5:]:
    if s == '...':
        print(s)
    elif s != GOAL:
        print(f"  Estado {s}: Acción -> {politica_optima.get(s, 'N/A')}")
    else:
        print(f"  Estado {s}: ¡META ALCANZADA!")