import numpy as np

# --- Funciones Esenciales ---
def sigmoide(x):
    return 1 / (1 + np.exp(-x))

def derivada_sigmoide(x):
    s = sigmoide(x)
    return s * (1 - s)

# --- Parámetros del Ejemplo ---
X = np.array([[0.5, 0.1]]) # Entrada
Y = np.array([[0.9]])      # Etiqueta Correcta
TASA_APRENDIZAJE = 0.1
EPOCHS = 100

# Pesos Iniciales (Definidos manualmente)
W_oculta = np.array([[0.1, 0.2], [0.3, 0.4]]) # 2x2
W_salida = np.array([[0.5], [0.6]])          # 2x1

print("==================================================")
print("     RETROPROPAGACIÓN: X PASOS DE APRENDIZAJE     ")
print("==================================================")

for epoch in range(1, EPOCHS + 1):
    
    # ----------------------------------------------------
    # FASE 1: PROPAGACIÓN ADELANTE (FORWARD PASS)
    # ----------------------------------------------------
    
    # Capa Oculta
    Z_oculta = np.dot(X, W_oculta) 
    A_oculta = sigmoide(Z_oculta)
    
    # Capa de Salida
    Z_salida = np.dot(A_oculta, W_salida)
    A_salida = sigmoide(Z_salida)
    
    # Error
    error = A_salida - Y
    loss = np.mean(error**2)

    # ----------------------------------------------------
    # FASE 2: RETROPROPAGACIÓN (BACKWARD PASS)
    # ----------------------------------------------------
    
    # 1. Delta de la Capa de Salida (D_salida)
    D_salida = error * derivada_sigmoide(Z_salida)

    # 2. Delta de la Capa Oculta (D_oculta)
    D_oculta = np.dot(D_salida, W_salida.T) * derivada_sigmoide(Z_oculta)

    # ----------------------------------------------------
    # FASE 3: ACTUALIZACIÓN DE PESOS
    # ----------------------------------------------------
    
    # Gradientes y Actualización para W_salida
    grad_W_salida = np.dot(A_oculta.T, D_salida)
    W_salida -= TASA_APRENDIZAJE * grad_W_salida

    # Gradientes y Actualización para W_oculta
    grad_W_oculta = np.dot(X.T, D_oculta)
    W_oculta -= TASA_APRENDIZAJE * grad_W_oculta
    
    # ----------------------------------------------------
    # MOSTRAR RESULTADOS DEL PASO
    # ----------------------------------------------------
    print(f"\n--- PASO {epoch} ---")
    print(f"PREDICCIÓN: {A_salida[0][0]:.6f}")
    print(f"ERROR (MSE): {loss:.8f}")
    print(f"W_salida actualizados:\n{W_salida.round(5)}")
    print(f"W_oculta actualizados:\n{W_oculta.round(5)}")
    
print("\n==================================================")
print("El error disminuye en cada paso, y los pesos se mueven")
print("hacia los valores óptimos para alcanzar la etiqueta 0.9.")