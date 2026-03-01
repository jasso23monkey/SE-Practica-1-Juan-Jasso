# --- 1. DEFINICIÓN DEL POMDP ---

# Conjunto de Estados (Ocultos)
ESTADOS = ['Limpio', 'Sucio']

# Creencia Inicial b0(s): El agente no sabe
b_actual = {'Limpio': 0.5, 'Sucio': 0.5}

# 1. Transiciones P(s' | s, a='Esperar')
T = {
    'Limpio': {'Limpio': 0.9, 'Sucio': 0.1}, # P(s'|s=L, a=E)
    'Sucio': {'Limpio': 0.2, 'Sucio': 0.8}  # P(s'|s=S, a=E)
}

# 2. Observación P(o | s')
O = {
    'OK': {'Limpio': 0.7, 'Sucio': 0.1},    # P(o='OK' | s')
    'RUIDO': {'Limpio': 0.3, 'Sucio': 0.9}  # P(o='RUIDO' | s')
}

# --- 2. FUNCIÓN DE ACTUALIZACIÓN DE CREENCIA ---

def actualizar_creencia(b_vieja, accion, observacion):
    """
    Calcula la nueva distribución de creencias b'(s') dado el estado de creencia b(s),
    una acción (implícita 'Esperar') y una observación.
    """
    b_nueva_sin_norm = {}
    
    # PASO A: PREDICCIÓN (P(s'))
    P_s_prime = {}
    for s_prime in ESTADOS:
        P_s_prime[s_prime] = 0
        for s in ESTADOS:
            # P(s') = Sum_s P(s'|s,a) * b(s)
            p_transicion = T[s][s_prime] 
            P_s_prime[s_prime] += p_transicion * b_vieja[s]

    # PASO B: ACTUALIZACIÓN (P(s' | o) y Normalización)
    normalizador = 0
    for s_prime in ESTADOS:
        # Numerador sin normalizar: P(o | s') * P(s')
        p_observacion = O[observacion][s_prime]
        numerador = p_observacion * P_s_prime[s_prime]
        
        b_nueva_sin_norm[s_prime] = numerador
        normalizador += numerador
        
    # Normalización para obtener la distribución final (b'(s'))
    b_nueva = {}
    for s_prime in ESTADOS:
        b_nueva[s_prime] = b_nueva_sin_norm[s_prime] / normalizador
        
    return b_nueva

# --- 3. SIMULACIÓN DE LA TOMA DE DECISIONES ---

print("--- POMDP: Simulación de la Creencia ---")
print(f"Creencia Inicial b0: {b_actual}")
print("====================================")

# Simulación 1: El robot toma la acción 'Esperar' y observa 'OK'
observacion_1 = 'OK'
b1 = actualizar_creencia(b_actual, 'Esperar', observacion_1)

print(f"1. Acción: Esperar. Observación: {observacion_1}")
print(f"   Nueva Creencia b1: P(L)={b1['Limpio']:.4f}, P(S)={b1['Sucio']:.4f}")

# Simulación 2: El robot toma la acción 'Esperar' de nuevo, y observa 'RUIDO'
observacion_2 = 'RUIDO'
b2 = actualizar_creencia(b1, 'Esperar', observacion_2)

print(f"\n2. Acción: Esperar. Observación: {observacion_2}")
print(f"   Nueva Creencia b2: P(L)={b2['Limpio']:.4f}, P(S)={b2['Sucio']:.4f}")

# Simulación 3: El robot toma la acción 'Esperar' de nuevo, y observa 'OK'
observacion_3 = 'OK'
b3 = actualizar_creencia(b2, 'Esperar', observacion_3)

print(f"\n3. Acción: Esperar. Observación: {observacion_3}")
print(f"   Nueva Creencia b3: P(L)={b3['Limpio']:.4f}, P(S)={b3['Sucio']:.4f}")