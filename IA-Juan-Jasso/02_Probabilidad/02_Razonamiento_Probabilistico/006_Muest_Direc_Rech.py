import random

# Definición de las probabilidades (CPTs)
P_R = 0.2       # P(Lluvia = Si)
P_S = 0.1       # P(Aspersor = Si)

P_W_dado_RS = { # P(Césped Húmedo = Si | Lluvia, Aspersor)
    ('Si', 'Si'): 0.99,
    ('Si', 'No'): 0.90,
    ('No', 'Si'): 0.90,
    ('No', 'No'): 0.01
}

def muestreo_directo(num_muestras):
    """Genera muestras siguiendo el orden R -> S -> W."""
    muestras = []
    for _ in range(num_muestras):
        # 1. Muestrear R (Lluvia)
        R = 'Si' if random.random() < P_R else 'No'
        
        # 2. Muestrear S (Aspersor)
        S = 'Si' if random.random() < P_S else 'No'
        
        # 3. Muestrear W (Césped Húmedo) dado R y S
        prob_W_Si = P_W_dado_RS[(R, S)]
        W = 'Si' if random.random() < prob_W_Si else 'No'
        
        muestras.append((R, S, W))
    return muestras

# Ejecución
NUM_MUESTRAS = 10000
muestras_directas = muestreo_directo(NUM_MUESTRAS)

# Contar la probabilidad aproximada de P(Lluvia=Si, Aspersor=Si, Húmedo=Si)
conteo = sum(1 for r, s, w in muestras_directas if r == 'Si' and s == 'Si' and w == 'Si')
P_R_S_W = conteo / NUM_MUESTRAS

print("--- 1. Muestreo Directo ---")
print(f"Número de muestras generadas: {NUM_MUESTRAS}")
print(f"Aproximación de P(R=Si, S=Si, W=Si): {P_R_S_W:.5f}")

# Usamos las mismas CPTs y la función de muestreo directo definida arriba.

def muestreo_por_rechazo(num_intentos, evidencia_W):
    """Genera muestras y rechaza aquellas inconsistentes con la evidencia W."""
    conteo_aceptadas = 0
    conteo_R_Si = 0
    
    for _ in range(num_intentos):
        # 1. Generar muestra (usando el muestreo directo)
        R = 'Si' if random.random() < P_R else 'No'
        S = 'Si' if random.random() < P_S else 'No'
        prob_W_Si = P_W_dado_RS[(R, S)]
        W_muestra = 'Si' if random.random() < prob_W_Si else 'No'
        
        # 2. Comprobar la Evidencia (Rechazo)
        if W_muestra == evidencia_W:
            # 3. Aceptar y Contar
            conteo_aceptadas += 1
            if R == 'Si':
                conteo_R_Si += 1
                
    # Inferencia: P(R=Si | W=Si) = Conteo(R=Si, W=Si) / Conteo(W=Si)
    if conteo_aceptadas > 0:
        P_R_dado_W = conteo_R_Si / conteo_aceptadas
    else:
        P_R_dado_W = 0.0

    return P_R_dado_W, conteo_aceptadas

# Ejecución
EVIDENCIA = 'Si' # El césped está húmedo
NUM_INTENTOS = 100000 # Necesitamos más intentos porque se rechazan muchas muestras

P_R_dado_W_aprox, muestras_aceptadas = muestreo_por_rechazo(NUM_INTENTOS, EVIDENCIA)

print("\n--- 2. Muestreo por Rechazo ---")
print(f"Evidencia: Césped Húmedo = {EVIDENCIA}")
print(f"Total de intentos de muestreo: {NUM_INTENTOS}")
print(f"Muestras aceptadas (Consistentes con la evidencia): {muestras_aceptadas}")
print(f"Tasa de rechazo: {1 - (muestras_aceptadas / NUM_INTENTOS):.2%}")
print(f"Aproximación de P(Lluvia=Si | Húmedo=Si): {P_R_dado_W_aprox:.4f}")