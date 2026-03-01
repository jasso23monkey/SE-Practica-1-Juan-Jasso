import numpy as np

# --- 1. Datos de Entrenamiento (Problema AND) ---
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
Y = np.array([0, 0, 0, 1]) # Salidas deseadas

# --- 2. Parámetros Comunes ---
EPOCHS = 20
TASA_APRENDIZAJE = 0.1

# --- 3. Funciones de Activación ---
def activacion_paso(z):
    # Aseguramos que la salida sea un array de NumPy (para compatibilidad)
    return np.where(z >= 0, 1, 0) 

def activacion_lineal(z):
    return z 

# --- 4. Inicialización y Entrenadores ---

def entrenar_neurona(X, Y, tipo_neurona):
    # Inicialización de pesos y sesgos (W y b)
    np.random.seed(42)
    W = np.random.uniform(low=-1.0, high=1.0, size=X.shape[1])
    b = 0.0
    
    errores = []

    for epoch in range(EPOCHS):
        error_total = 0
        
        for x, y in zip(X, Y):
            # 1. Propagación Adelante
            Z = np.dot(x, W) + b
            
            # --- Diferencia en el Cálculo de Salida y Error ---
            if tipo_neurona == 'Perceptron':
                salida_predicha = activacion_paso(Z)
                error = y - salida_predicha          
            elif tipo_neurona == 'ADALINE':
                salida_predicha = activacion_lineal(Z)
                error = y - salida_predicha            
            
            # SOLUCIÓN: Convertir 'error' a float estándar. 
            # Esto maneja el caso de que error pueda ser un array de 0 dimensiones.
            error_escalar = float(error)
            
            # 2. Actualización de Pesos (Regla Delta/Perceptrón)
            # W += TASA_APRENDIZAJE * error * x
            W += TASA_APRENDIZAJE * error_escalar * x
            b += TASA_APRENDIZAJE * error_escalar * 1 
            
            error_total += error_escalar**2 # Usar el error como escalar para el MSE
        
        errores.append(error_total / len(X))
        
    return W, b, errores

# --- 5. Ejecución y Comparación de Entrenamiento ---

W_p, b_p, errores_p = entrenar_neurona(X, Y, 'Perceptron')
W_a, b_a, errores_a = entrenar_neurona(X, Y, 'ADALINE')

print("=============================================")
print("  COMPARATIVA DE APRENDIZAJE: Perceptrón vs ADALINE")
print("=============================================")
print(f"Final W (Perceptrón): {W_p}, b: {b_p:.3f}")
print(f"Final W (ADALINE): {W_a}, b: {b_a:.3f}")
print("-" * 50)
print(f"Error final (Perceptrón, MSE): {errores_p[-1]:.4f}")
print(f"Error final (ADALINE, MSE): {errores_a[-1]:.4f}")

# --- 6. Nota sobre MADALINE ---
print("\nNota sobre MADALINE:")
print("MADALINE es una arquitectura que conecta varias ADALINEs. Para implementar MADALINE,")
print("necesitaríamos implementar capas ocultas y un algoritmo de aprendizaje más complejo,")
print("como la **Retropropagación**, ya que su regla de entrenamiento original era heurística y limitada.")