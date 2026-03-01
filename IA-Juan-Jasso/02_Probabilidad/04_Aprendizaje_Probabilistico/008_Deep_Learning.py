import numpy as np

# --- A. Funciones de Activación ---

def sigmoide(x):
    """Función de activación Sigmoide: S(x) = 1 / (1 + e^-x)"""
    return 1 / (1 + np.exp(-x))

def derivada_sigmoide(x):
    """Derivada de la Sigmoide para la retropropagación: S'(x) = S(x) * (1 - S(x))"""
    s = sigmoide(x)
    return s * (1 - s)

# --- B. Datos de Entrenamiento (Problema XOR) ---
# XOR: 0 XOR 0 = 0, 0 XOR 1 = 1, 1 XOR 0 = 1, 1 XOR 1 = 0
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]]) # Entradas (4 ejemplos, 2 características)
Y = np.array([[0], [1], [1], [0]])            # Salidas (etiquetas correctas)

# --- C. Parámetros de la Red ---
N_ENTRADA = 2     # Número de características de entrada
N_OCULTA = 4      # Número de neuronas en la capa oculta (ajustable)
N_SALIDA = 1      # Número de neuronas de salida (clasificación binaria)
TASA_APRENDIZAJE = 0.1
EPOCHS = 10000    # Número de iteraciones de entrenamiento

# Inicializar pesos y sesgos aleatoriamente para evitar simetría.

# Pesos y sesgos de la Capa Oculta
W_oculta = np.random.uniform(size=(N_ENTRADA, N_OCULTA)) # Matriz 2x4
B_oculta = np.zeros((1, N_OCULTA))                       # Vector 1x4

# Pesos y sesgos de la Capa de Salida
W_salida = np.random.uniform(size=(N_OCULTA, N_SALIDA)) # Matriz 4x1
B_salida = np.zeros((1, N_SALIDA))                       # Vector 1x1

print("Iniciando entrenamiento...")
for i in range(EPOCHS):
    
    # =================================================================
    # PASO 1: PROPAGACIÓN HACIA ADELANTE (FORWARD PASS)
    # =================================================================
    
    # 1. Capa Oculta
    # Z_oculta = X . W_oculta + B_oculta
    Z_oculta = np.dot(X, W_oculta) + B_oculta
    
    # A_oculta = Sigmoide(Z_oculta)
    A_oculta = sigmoide(Z_oculta)
    
    # 2. Capa de Salida
    # Z_salida = A_oculta . W_salida + B_salida
    Z_salida = np.dot(A_oculta, W_salida) + B_salida
    
    # PREDICCIÓN (A_salida = Sigmoide(Z_salida))
    A_salida = sigmoide(Z_salida)
    
    # =================================================================
    # PASO 2: CÁLCULO DE ERROR y RETROPROPAGACIÓN (BACKPROPAGATION)
    # =================================================================
    
    # 1. Error en la Capa de Salida
    # ERROR = (A_salida - Y) 
    error_salida = A_salida - Y
    
    # 2. Delta de la Capa de Salida (Gradiente del Error * Derivada del Sigmoide)
    # Delta_salida = ERROR * S'(Z_salida)
    D_salida = error_salida * derivada_sigmoide(Z_salida)
    
    # 3. Delta de la Capa Oculta (Propagar el Delta hacia atrás)
    # Delta_oculta = Delta_salida . W_salida_transpuesta * S'(Z_oculta)
    D_oculta = np.dot(D_salida, W_salida.T) * derivada_sigmoide(Z_oculta)
    
    # 4. Actualización de Pesos y Sesgos (Descenso de Gradiente)
    
    # Tasa_Aprendizaje * Promedio(Input * Delta)
    
    # Actualizar W_salida (Gradiente: A_oculta_transpuesta . D_salida)
    W_salida -= TASA_APRENDIZAJE * np.dot(A_oculta.T, D_salida)
    B_salida -= TASA_APRENDIZAJE * np.sum(D_salida, axis=0, keepdims=True)
    
    # Actualizar W_oculta (Gradiente: X_transpuesta . D_oculta)
    W_oculta -= TASA_APRENDIZAJE * np.dot(X.T, D_oculta)
    B_oculta -= TASA_APRENDIZAJE * np.sum(D_oculta, axis=0, keepdims=True)
    
    # Mostrar el error cada 1000 epochs
    if i % 1000 == 0:
        loss = np.mean(np.square(error_salida))
        print(f"Epoch {i}: Error (MSE) = {loss:.6f}")

# --- 4. Prueba Final ---

# Recalcular la propagación hacia adelante con los pesos aprendidos
Z_oculta_final = np.dot(X, W_oculta) + B_oculta
A_oculta_final = sigmoide(Z_oculta_final)
Z_salida_final = np.dot(A_oculta_final, W_salida) + B_salida
PREDICCIONES = sigmoide(Z_salida_final)

# Redondear las predicciones a 0 o 1
PREDICCIONES_BINARIAS = np.round(PREDICCIONES)

print("\n=============================================")
print("  RESULTADO FINAL (Problema XOR)")
print("=============================================")
print("Entrada (X) | Etiqueta (Y) | Predicción (A_salida)")
print("-" * 50)
for x_val, y_val, pred_val in zip(X, Y, PREDICCIONES):
    print(f"  {x_val}   |    {y_val[0]}       |   {pred_val[0]:.4f} (Clase: {np.round(pred_val[0])})")