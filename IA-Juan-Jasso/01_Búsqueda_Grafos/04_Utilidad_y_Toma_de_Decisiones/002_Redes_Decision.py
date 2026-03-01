#import numpy as np

# --- INCERTIDUMBRE (Chance Node) ---
# Probabilidad del Clima Real P(Clima)
# Suponemos que la probabilidad de lluvia es 0.4 (40%)
P_CLIMA = {
    'Lluvia': 0.4,
    'Sol': 0.6
}

# --- UTILIDAD (Utility Node) ---
# U(Decisión, Clima)
# La utilidad depende de la combinación de la acción del agente y el clima real.

UTILIDAD_TABLA = {
    # Si Llevo Paraguas (LP)
    'LP': {
        'Lluvia': 50,  # Alta Utilidad: Seco y cubierto
        'Sol': 10     # Baja Utilidad: Cargar peso innecesariamente
    },
    # Si No Llevo Paraguas (NLP)
    'NLP': {
        'Lluvia': -100, # Utilidad Negativa: Mojarse mucho
        'Sol': 80      # Máxima Utilidad: Cómodo y soleado
    }
}

# --- 3. ALGORITMO: PRINCIPIO DE MÁXIMA UTILIDAD ESPERADA (MEU) ---

def resolver_red_decision():
    """Calcula la Utilidad Esperada (EU) para cada acción y determina la óptima."""
    
    acciones = ['LP', 'NLP']
    utilidades_esperadas = {}
    
    print("--- 1. Cálculo de la Utilidad Esperada (EU) ---")
    
    for accion in acciones:
        eu = 0
        
        # Iterar sobre todos los posibles estados de incertidumbre (Clima)
        for clima, p_clima in P_CLIMA.items():
            
            # Obtener la utilidad de la combinación (Acción, Clima)
            utilidad = UTILIDAD_TABLA[accion][clima]
            
            # EU += P(Clima) * U(Acción, Clima)
            eu_contribucion = p_clima * utilidad
            eu += eu_contribucion
            
            print(f"  EU({accion} | {clima}): P({clima})={p_clima} * U={utilidad} = {eu_contribucion:.2f}")

        utilidades_esperadas[accion] = eu
        print(f"  -> EU Total({accion}): {eu:.2f}\n")

    # 2. Elegir la acción que maximiza la utilidad esperada
    mejor_accion = max(utilidades_esperadas, key=utilidades_esperadas.get)
    meu = utilidades_esperadas[mejor_accion]
    
    print("="*50)
    print("--- 2. Decisión del Agente (MEU) ---")
    print(f"EU(Llevar Paraguas): {utilidades_esperadas['LP']:.2f}")
    print(f"EU(No Llevar Paraguas): {utilidades_esperadas['NLP']:.2f}")
    print(f"La acción óptima es: {mejor_accion}")
    print(f"Máxima Utilidad Esperada (MEU) = {meu:.2f}")
    
    return mejor_accion, meu

# Ejecución de la Red de Decisión
resolver_red_decision()