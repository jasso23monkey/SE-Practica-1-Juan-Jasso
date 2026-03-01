import numpy as np
import random

# --- 1. CONFIGURACIÓN ---

ESTADOS = ['S0', 'S1', 'S2', 'S3']
ACCIONES = ['I', 'D']  # Izquierda, Derecha

# Parámetros de Aprendizaje
GAMMA = 0.9      # Factor de Descuento
ALPHA = 0.1      # Tasa de Aprendizaje
EPSILON = 0.1    # Tasa de Exploración
EPISODIOS = 500  

RECOMPENSA_META = 10
RECOMPENSA_PASO = -1

# Inicializar la Q-Table a ceros
Q = {}
for s in ESTADOS:
    Q[s] = {'I': 0.0, 'D': 0.0}

# --- 2. FUNCIONES DE TRANSICIÓN Y POLÍTICA ---

def get_next_state(s, a):
    """Determina el siguiente estado s' (Transiciones Deterministas)"""
    if a == 'D':
        if s == 'S0': return 'S1'
        if s == 'S1': return 'S2'
        if s == 'S2': return 'S3'
        return s
    else: # a == 'I'
        if s == 'S1': return 'S0'
        if s == 'S2': return 'S1'
        if s == 'S3': return 'S2'
        return s

def choose_action(s):
    """Política epsilon-greedy: Explora con prob. epsilon, Explota con 1-epsilon."""
    if random.random() < EPSILON:
        # Exploración: elige una acción aleatoria
        return random.choice(ACCIONES)
    else:
        # Explotación: elige la acción con el Q-Value más alto
        q_values = Q[s]
        return max(q_values, key=q_values.get)

# --- 3. ALGORITMO PRINCIPAL DE SARSA ---

for episodio in range(EPISODIOS):
    s = 'S0'
    
    # 1. Elegir la primera acción 'a' usando epsilon-greedy
    a = choose_action(s)
    
    while s != 'S3':
        
        # 2. Observar la Transición (s, a, r, s')
        s_prime = get_next_state(s, a)
        
        r = RECOMPENSA_PASO
        if s_prime == 'S3':
            r = RECOMPENSA_META
            Q_s_prime_a_prime = 0.0 # Valor de Q en estado terminal es 0
            a_prime = None # No hay acción siguiente en terminal
        else:
            # 3. Elegir la siguiente acción 'a'' (la clave SARSA)
            a_prime = choose_action(s_prime)
            # 4. Obtener el valor Q(s', a') para la actualización
            Q_s_prime_a_prime = Q[s_prime][a_prime]
        
        # 5. ACTUALIZACIÓN DEL Q-VALUE (Fórmula de SARSA)
        
        # Objetivo TD: r + gamma * Q(s', a')
        objetivo_td = r + GAMMA * Q_s_prime_a_prime
        
        # Error TD: Objetivo TD - Q(s, a)
        error_td = objetivo_td - Q[s][a]
        
        # Actualización: Q(s, a) <- Q(s, a) + alpha * Error TD
        Q[s][a] += ALPHA * error_td
        
        # Mover al siguiente paso (s <- s', a <- a')
        s = s_prime
        a = a_prime

# --- 4. EXTRACCIÓN DE LA POLÍTICA ÓPTIMA ---

def extraer_politica(Q):
    """Devuelve la acción óptima (π*(s)) para cada estado."""
    politica = {}
    for s in ESTADOS:
        if s == 'S3':
            politica[s] = 'TERMINAL'
        else:
            # La política óptima es la acción que maximiza Q(s, a)
            politica[s] = max(Q[s], key=Q[s].get)
    return politica

# --- 5. RESULTADOS FINALES ---

politica_optima = extraer_politica(Q)

print("--- APRENDIZAJE POR REFUERZO ACTIVO: SARSA ---")
print(f"Parámetros: α={ALPHA}, γ={GAMMA}, ε={EPSILON}")
print("\nTABLA Q (Valores de Acción-Estado):")
for s, q_values in Q.items():
    print(f"  {s}: {q_values}")

print("\nPOLÍTICA ÓPTIMA APRENDIDA (π*(s)):")
print(politica_optima)