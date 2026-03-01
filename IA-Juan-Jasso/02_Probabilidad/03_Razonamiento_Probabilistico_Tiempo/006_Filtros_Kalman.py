import numpy as np

# --- 1. Parámetros del Filtro ---
dt = 0.1  # Intervalo de tiempo (segundos)

# --- A. Matrices de Modelo de Estado ---

# Matriz de Transición de Estado (F):
# x_k = F * x_{k-1} + ...
# Posición: p_k = p_{k-1} + v_{k-1} * dt
# Velocidad: v_k = v_{k-1}
F = np.array([[1, dt], 
              [0, 1]])

# Matriz de Observación (H): Medimos solo la posición
# z_k = H * x_k + ...
H = np.array([[1, 0]])

# Matriz de Covarianza de Ruido de Proceso (Q):
# Ruido pequeño en la aceleración (0.01)
Q = np.array([[0.01, 0], 
              [0, 0.01]])

# Matriz de Covarianza de Ruido de Medición (R):
# Ruido de medición del sensor (1.0)
R = np.array([[1.0]]) 

# --- B. Inicialización ---

# Estado Inicial Estimado (x_hat_0)
x_hat = np.array([[0], [0]]) # [Posición inicial 0, Velocidad inicial 0]

# Covarianza Inicial Estimada (P_0): Alta incertidumbre inicial
P = np.array([[100, 0], 
              [0, 100]])

def filtro_kalman(z_k, x_hat_k_minus_1, P_k_minus_1, F, H, Q, R):
    """
    Realiza un paso completo del Filtro de Kalman.
    z_k: Medición actual
    """
    
    # --- FASE 1: PREDICCIÓN (PROYECCIÓN) ---
    
    # 1. Predicción del Estado (x_hat_k_menos)
    x_hat_k_menos = F @ x_hat_k_minus_1
    
    # 2. Predicción de la Covarianza (P_k_menos)
    P_k_menos = F @ P_k_minus_1 @ F.T + Q
    
    
    # --- FASE 2: ACTUALIZACIÓN (CORRECCIÓN) ---
    
    # 3. Ganancia de Kalman (K_k)
    # K_k = P_k_menos * H.T * inv( H * P_k_menos * H.T + R )
    S_k = H @ P_k_menos @ H.T + R  # Covarianza de la Innovación
    K_k = P_k_menos @ H.T @ np.linalg.inv(S_k)
    
    # 4. Actualización del Estado (x_hat_k)
    innovacion = z_k - H @ x_hat_k_menos # Diferencia entre medición y predicción
    x_hat_k = x_hat_k_menos + K_k @ innovacion
    
    # 5. Actualización de la Covarianza (P_k)
    P_k = (np.eye(P_k_menos.shape[0]) - K_k @ H) @ P_k_menos
    
    return x_hat_k, P_k, K_k

# --- Simulación de Datos (Movimiento real y mediciones ruidosas) ---
# El objeto se mueve a velocidad constante (1.0 m/s)
VELOCIDAD_REAL = 1.0
NUM_PASOS = 50

# Generar la trayectoria real y las observaciones
posicion_real = np.arange(NUM_PASOS) * dt * VELOCIDAD_REAL
# Las mediciones ruidosas (Posición real + Ruido gaussiano)
np.random.seed(42) 
mediciones = posicion_real + np.random.normal(0, np.sqrt(R[0, 0]), size=NUM_PASOS)


# --- Ejecución del Bucle ---
posiciones_estimadas = []
posiciones_reales = []

# x_hat y P se actualizan en cada paso
for k in range(NUM_PASOS):
    z_k = np.array([[mediciones[k]]]) # Medición en el paso k
    
    # Aplicar el filtro
    x_hat, P, K = filtro_kalman(z_k, x_hat, P, F, H, Q, R)
    
    # Almacenar la posición estimada (primer elemento del vector de estado)
    posiciones_estimadas.append(x_hat[0, 0])
    posiciones_reales.append(posicion_real[k])


# --- Visualización del Resultado (requiere matplotlib) ---
import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.plot(posiciones_reales, label='Posición Real (Oculta)', color='green', linewidth=2)
plt.scatter(range(NUM_PASOS), mediciones, label='Mediciones Ruidosas (Z_k)', color='red', alpha=0.5, marker='.')
plt.plot(posiciones_estimadas, label='Estimación del Filtro de Kalman (X_hat_k)', color='blue', linewidth=2, linestyle='--')
plt.title('Seguimiento de Posición 1D con Filtro de Kalman')
plt.xlabel('Paso de Tiempo')
plt.ylabel('Posición (metros)')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.6)
plt.show()

# --- Conclusión de la Ganancia de Kalman ---
print("\n--- Conclusión del Filtro ---")
print(f"Ganancia de Kalman (K_k) en el último paso:\n{K}")
print("El filtro usa esta Ganancia para ponderar la nueva medición frente a su predicción.")
print("Un valor alto en K indica que el filtro confía más en la nueva medición Z_k.")