import numpy as np
import random

# --- 1. CONFIGURACIÓN ---
ALPHA = 0.1      # Tasa de aprendizaje (alpha)
EPISODIOS = 500  # Número de episodios
GAMMA = 1.0      # Sin descuento (Monte Carlo)

# Inicializar el parámetro de la política (theta)
# Theta controla la preferencia por la acción 'Derecha'
theta = 0.0 

# --- 2. FUNCIÓN DE POLÍTICA (Pi) ---

def politica_prob(theta):
    """Calcula la probabilidad de elegir 'Derecha' usando la función Sigmoide."""
    # Usamos la Sigmoide para mapear theta (cualquier número real) a una probabilidad (0 a 1)
    prob_derecha = 1 / (1 + np.exp(-theta))
    return prob_derecha

def elegir_accion(prob_derecha):
    """Elige una acción basada en la probabilidad actual."""
    if random.random() < prob_derecha:
        return 'D'
    return 'I'

# --- 3. ALGORITMO REINFORCE SIMPLIFICADO ---

def actualizar_politica(accion_tomada, recompensa_G):
    """
    Implementa el paso clave de Búsqueda de Política usando el gradiente.
    REINFORCE usa el retorno total (G) para ajustar theta.
    """
    global theta
    
    # 1. Calcular la probabilidad actual de ir a la derecha (p)
    p_derecha = politica_prob(theta)
    
    # 2. Calcular el score (∇log π(A|S; θ)): La sensibilidad del log-prob a theta.
    # Para la Sigmoide: ∇log π(A|S; θ) = (1 - π) si A=D, y -π si A=I
    
    if accion_tomada == 'D':
        # Score_Derecha = (1 - p)
        score_gradiente = (1 - p_derecha)
    else: # accion_tomada == 'I'
        # Score_Izquierda = -(p)
        score_gradiente = -p_derecha
        
    # 3. Aplicar la Regla de Actualización de REINFORCE
    # θ ← θ + α * G * ∇log π(A|S; θ)
    ajuste = ALPHA * recompensa_G * score_gradiente
    theta += ajuste
    
    return ajuste

# --- 4. BUCLE PRINCIPAL DE APRENDIZAJE ---

print("--- BÚSQUEDA DE POLÍTICA: REINFORCE (Gradiente) ---")

for episodio in range(EPISODIOS):
    
    # El agente inicia en S0 y termina en el siguiente paso
    
    # 1. Elige una acción basada en la política actual
    prob_derecha_actual = politica_prob(theta)
    accion = elegir_accion(prob_derecha_actual)
    
    # 2. Obtiene Recompensa (G)
    if accion == 'D':
        G = 1  # Retorno Total = 1
    else:
        G = 0  # Retorno Total = 0
        
    # 3. Ajusta la Política
    ajuste = actualizar_politica(accion, G)
    
    # Registro de datos
    if episodio % (EPISODIOS / 10) == 0:
        print(f"Episodio {episodio:04d}: θ={theta:.4f} | Prob(D)={prob_derecha_actual:.4f} | Ajuste={ajuste:.6f}")

# --- 5. RESULTADOS FINALES ---

prob_final = politica_prob(theta)

print("\n" + "="*55)
print("RESULTADOS FINALES DE BÚSQUEDA DE POLÍTICA:")
print(f"Parámetro final (θ): {theta:.4f}")
print(f"Probabilidad final de ir a la Derecha (π*(D)): {prob_final:.4f}")
print("===========================================")

# Conclusión
if prob_final > 0.95:
    print(" La política convergió exitosamente a la acción óptima (Derecha).")
else:
    print(" La política no convergió completamente.")