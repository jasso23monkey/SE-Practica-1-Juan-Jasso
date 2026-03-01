import random
import numpy as np

# --- 1. CONFIGURACIÓN DEL MDP Y PARÁMETROS DE APRENDIZAJE ---

ESTADOS = ['S0', 'S1', 'S2', 'S3']
RECOMPENSA_META = 10
RECOMPENSA_PASO = -1
GAMMA = 0.8     # Factor de Descuento
ALPHA = 0.01      # Tasa de Aprendizaje (para la actualización TD)
EPISODIOS = 1000  # Número de trayectorias a simular

# Política Fija (Pasiva): Siempre ir a la Derecha
POLITICA = {
    'S0': 'D',
    'S1': 'D',
    'S2': 'D',
    'S3': None  # Estado Terminal
}

# Transiciones Deterministas (El agente siempre llega a donde apunta la política)
TRANSICIONES = {
    'S0': 'S1',
    'S1': 'S2',
    'S2': 'S3'
}

# Inicializar la Función de Valor V(s) a cero
V = {s: 0.0 for s in ESTADOS}

# --- 2. SIMULACIÓN DE EPISODIOS Y APRENDIZAJE TD(0) ---

def simular_episodio_td0():
    """Simula un episodio siguiendo la política fija y actualiza V(s) usando TD(0)."""
    
    estado_actual = 'S0' # Siempre inicia en S0
    
    while estado_actual != 'S3':
        s = estado_actual
        accion = POLITICA[s]
        
        # 1. Ejecutar la acción y observar la transición (s, a, r, s')
        
        # Determinar el estado siguiente (s') y la recompensa (r)
        s_prime = TRANSICIONES[s]
        r = RECOMPENSA_PASO 
        
        if s_prime == 'S3':
            r = RECOMPENSA_META 
            V_s_prime = 0.0 # V(S3) es 0 en TD para estados absorbentes (no hay futuro)
        else:
            V_s_prime = V[s_prime]
            
        # 2. CALCULAR EL ERROR TD Y ACTUALIZAR V(s)
        
        # Objetivo de TD (r + gamma * V(s'))
        objetivo_td = r + GAMMA * V_s_prime
        
        # Error TD = Objetivo TD - V(s)
        error_td = objetivo_td - V[s]
        
        # Actualización: V(s) <- V(s) + alpha * Error TD
        V[s] = V[s] + ALPHA * error_td
        
        # Avanzar al siguiente estado
        estado_actual = s_prime
        
    return V

# --- 3. EJECUCIÓN DEL APRENDIZAJE ---

print("--- APRENDIZAJE PASIVO: EVALUACIÓN DE POLÍTICA CON TD(0) ---")

for episodio in range(1, EPISODIOS + 1):
    simular_episodio_td0()
    
    if episodio % (EPISODIOS // 10) == 0 or episodio == 1:
        v_str = ', '.join([f'{s}={V[s]:.4f}' for s in ESTADOS])
        print(f"Episodio {episodio:03d}: {v_str}")

# --- 4. RESULTADOS FINALES ---

# Valor Teórico (Convergencia Esperada):
# V(S3) = 10 (Recompensa final)
# V(S2) = R + γ*V(S3) = -1 + 0.9*10 = 8.0
# V(S1) = R + γ*V(S2) = -1 + 0.9*8.0 = 6.2
# V(S0) = R + γ*V(S1) = -1 + 0.9*6.2 = 4.58

print("\n" + "="*50)
print("VALOR FINAL ESTIMADO V^π(s):")
print(f"V(S0): {V['S0']:.4f} (Teórico: 4.58)")
print(f"V(S1): {V['S1']:.4f} (Teórico: 6.20)")
print(f"V(S2): {V['S2']:.4f} (Teórico: 8.00)")
print(f"V(S3): {V['S3']:.4f} (Teórico: 0.00 en TD(0) por ser absorbente)")