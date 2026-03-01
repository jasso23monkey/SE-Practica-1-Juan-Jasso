# --- 1. DEFINICIÓN DE FACTORES (CPTs) ---

# P(D)
F_D = {'Alta': 0.6, 'Baja': 0.4}

# P(I)
F_I = {'Alta': 0.7, 'Baja': 0.3}

# P(L | I)
F_L_dado_I = {
    ('Alta', 'Fuerte'): 0.8,  # P(L=Fuerte | I=Alta)
    ('Alta', 'Débil'): 0.2,
    ('Baja', 'Fuerte'): 0.3,   # P(L=Fuerte | I=Baja)
    ('Baja', 'Débil'): 0.7
}

# P(G | D, I)
F_G_dado_DI = {
    ('Alta', 'Alta', 'A'): 0.3, # P(G=A | D=Alta, I=Alta)
    ('Alta', 'Baja', 'A'): 0.05,
    ('Baja', 'Alta', 'A'): 0.9,
    ('Baja', 'Baja', 'A'): 0.5,
    ('Alta', 'Alta', 'B'): 0.7, # P(G=B | D=Alta, I=Alta)
    ('Alta', 'Baja', 'B'): 0.95,
    ('Baja', 'Alta', 'B'): 0.1,
    ('Baja', 'Baja', 'B'): 0.5
}

# --- FUNCIÓN DE CÁLCULO DE FACTORES ---

def get_cpt_value(factor, keys):
    """Obtiene el valor de un factor (CPT) dada una tupla de claves."""
    try:
        # P(D) o P(I)
        if len(keys) == 1:
            return factor[keys[0]]
        # P(L|I) o P(G|D,I)
        return factor[keys]
    except KeyError:
        # Se asume que la probabilidad del estado opuesto es 1 - el valor conocido.
        # Esto simplifica el código, asumiendo CPTs binarias.
        if len(keys) == 2: # P(L|I)
            keys_op = (keys[0], 'Débil' if keys[1] == 'Fuerte' else 'Fuerte')
            return 1.0 - factor[keys_op]
        return 0.0 # Error o estado no contemplado si las claves son más complejas
    
# --- 2. ELIMINACIÓN DE VARIABLES ---

# Evidencia fijada: G='A'
G_EVIDENCIA = 'A'

# --- A. ELIMINAR VARIABLE D (DIFICULTAD) ---
# Sumamos D de todos los factores que contienen a D: {P(D), P(G | D, I)}
# El resultado es un nuevo factor temporal: T1(G, I) = SUM_D [ P(G | D, I) * P(D) ]

T1 = {}  # Factor T1: P(G=A, I)
for I_state in ['Alta', 'Baja']:
    suma_D = 0.0
    for D_state in ['Alta', 'Baja']:
        # Factor P(G=A | D, I)
        key_gdi = (D_state, I_state, G_EVIDENCIA)
        prob_g_dado_di = F_G_dado_DI.get(key_gdi, 1.0 - F_G_dado_DI.get(key_gdi[:-1] + ('B',), 0.0))
        
        # Factor P(D)
        prob_d = get_cpt_value(F_D, (D_state,))
        
        suma_D += prob_g_dado_di * prob_d
        
    T1[I_state] = suma_D

print("--- Eliminación de Variables ---")
print(f"Paso 1: Eliminado D. Nuevo Factor T1(I) [P(G=A, I)]: {T1}")
# T1['Alta'] = P(G=A|D=Alta,I=Alta)P(D=Alta) + P(G=A|D=Baja,I=Alta)P(D=Baja)
#            = (0.3 * 0.6) + (0.9 * 0.4) = 0.18 + 0.36 = 0.54
# T1['Baja'] = (0.05 * 0.6) + (0.5 * 0.4) = 0.03 + 0.20 = 0.23


# --- B. ELIMINAR VARIABLE I (INTELIGENCIA) ---
# Multiplicamos los factores restantes que contienen a I: {T1(I), P(I), P(L | I)}
# Luego sumamos I: T2(L) = SUM_I [ P(L | I) * P(I) * T1(I) ]

T2 = {} # Factor T2: P(L, G=A)
for L_state in ['Fuerte', 'Débil']:
    suma_I = 0.0
    for I_state in ['Alta', 'Baja']:
        # Factor P(L | I)
        prob_l_dado_i = get_cpt_value(F_L_dado_I, (I_state, L_state))
        
        # Factor P(I)
        prob_i = get_cpt_value(F_I, (I_state,))
        
        # Factor T1(I)
        prob_t1 = T1[I_state]
        
        suma_I += prob_l_dado_i * prob_i * prob_t1
        
    T2[L_state] = suma_I

print(f"Paso 2: Eliminado I. Nuevo Factor T2(L) [P(L, G=A)]: {T2}")
# T2['Fuerte'] = P(L=F|I=Alta)P(I=Alta)T1(I=Alta) + P(L=F|I=Baja)P(I=Baja)T1(I=Baja)
#              = (0.8 * 0.7 * 0.54) + (0.3 * 0.3 * 0.23)
#              = 0.3024 + 0.0207 = 0.3231


# --- C. NORMALIZACIÓN Y RESULTADO FINAL ---

# El resultado no normalizado es T2.
normalizador = T2['Fuerte'] + T2['Débil']
P_L_dado_G = T2['Fuerte'] / normalizador

print("-" * 50)
print(f"Normalizador P(G=A) (Suma de T2): {normalizador:.4f}")
print(f"Probabilidad Final P(L=Fuerte | G=A): {P_L_dado_G:.4f}")