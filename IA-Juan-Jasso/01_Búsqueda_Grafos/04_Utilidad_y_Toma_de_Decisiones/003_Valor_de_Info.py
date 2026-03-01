# --- PARÁMETROS DEL PROBLEMA ---

# 1. Probabilidades Iniciales P(Estado)
P_INICIAL = {'F': 0.6, 'D': 0.4}

# 2. Utilidades U(Acción, Estado)
UTILIDADES = {
    'Inv': {'F': 100, 'D': -50},
    'NInv': {'F': 0, 'D': 0}
}

# 3. Probabilidades de la Evidencia P(Evidencia)
P_EVIDENCIA = {'P': 0.5, 'N': 0.5}

# 4. Probabilidades Condicionales P(Estado | Evidencia)
P_CONDICIONAL = {
    'P': {'F': 0.8, 'D': 0.2}, # P(Estado | Informe Positivo)
    'N': {'F': 0.2, 'D': 0.8}  # P(Estado | Informe Negativo)
}

# --- FUNCIÓN DE CÁLCULO DE UTILIDAD ESPERADA ---

def calcular_eu(accion, P_estado):
    """Calcula EU(accion) dada una distribución de probabilidad del estado."""
    eu = 0
    for estado, p in P_estado.items():
        eu += p * UTILIDADES[accion][estado]
    return eu

# --- 1. CÁLCULO DE LA UTILIDAD SIN INFORMACIÓN (MEU(alpha)) ---

def calcular_meu_sin_info():
    eu_inv = calcular_eu('Inv', P_INICIAL)
    eu_ninv = calcular_eu('NInv', P_INICIAL)
    
    meu_sin = max(eu_inv, eu_ninv)
    
    print("--- 1. Sin Información ---")
    print(f"EU(Inv) = {eu_inv:.2f}")
    print(f"EU(NInv) = {eu_ninv:.2f}")
    print(f"MEU(sin info) = {meu_sin:.2f}")
    return meu_sin

# --- 2. CÁLCULO DE LA UTILIDAD CON INFORMACIÓN (EU(E)) ---

def calcular_eu_con_info():
    eu_con = 0
    
    print("\n--- 2. Con Información (EU(E)) ---")
    
    for evidencia, p_evidencia in P_EVIDENCIA.items():
        # A. Calcular EU(accion | evidencia)
        P_estado_condicional = P_CONDICIONAL[evidencia]
        
        eu_inv_cond = calcular_eu('Inv', P_estado_condicional)
        eu_ninv_cond = calcular_eu('NInv', P_estado_condicional)
        
        # B. Elegir la mejor acción bajo la evidencia
        meu_evidencia = max(eu_inv_cond, eu_ninv_cond)
        
        print(f"Si Informe es {evidencia} (P={p_evidencia:.1f}):")
        print(f"  EU(Inv | {evidencia}) = {eu_inv_cond:.2f}")
        print(f"  EU(NInv | {evidencia}) = {eu_ninv_cond:.2f}")
        print(f"  Decisión: {'Inv' if eu_inv_cond > eu_ninv_cond else 'NInv'} | MEU({evidencia}) = {meu_evidencia:.2f}")
        
        # C. Ponderar por la probabilidad de obtener esa evidencia
        eu_con += p_evidencia * meu_evidencia
        
    print(f"\nEU(Con info) = {eu_con:.2f}")
    return eu_con

# --- 3. CÁLCULO DEL VOI ---

def calcular_voi():
    meu_sin = calcular_meu_sin_info()
    eu_con = calcular_eu_con_info()
    
    voi = eu_con - meu_sin
    
    print("\n" + "="*50)
    print("--- 3. VALOR DE LA INFORMACIÓN (VOI) ---")
    print("VOI = EU(Con info) - MEU(sin info)")
    print(f"VOI = {eu_con:.2f} - {meu_sin:.2f} = {voi:.2f}")
    
    if voi > 0:
        print(f"-> La información VALE {voi:.2f} unidades de utilidad.")
    else:
        print("-> La información NO tiene valor.")
    
# Ejecución
calcular_voi()