import numpy as np

# --- 1. Definición de la Función de Activación (Función Escalón) ---

def funcion_activacion(z):
    """
    Simula el 'disparo' de la neurona.
    Si la suma ponderada (z) supera el umbral (0), devuelve 1, si no, devuelve 0.
    """
    return 1 if z >= 0 else 0

# --- 2. Parámetros del Perceptrón (Pesos y Sesgo) ---
# Estos parámetros se aprenden en una red neuronal real (entrenamiento), 
# pero aquí los definimos manualmente para resolver AND.

# Pesos (W): Miden la importancia de cada entrada.
W = np.array([0.5, 0.5]) 
# Sesgo (b): El umbral negativo (si el umbral es 0.7, el sesgo es -0.7).
B = -0.7 

# --- 3. Datos de Prueba (Problema AND) ---
# AND: Solo es 1 si ambas entradas son 1.
X_prueba = np.array([
    [0, 0], # Esperado: 0
    [0, 1], # Esperado: 0
    [1, 0], # Esperado: 0
    [1, 1]  # Esperado: 1
])

# --- 4. Función de Propagación (FORWARD PASS) ---

def perceptron(x, W, B):
    """
    Calcula la suma ponderada y aplica la función de activación.
    """
    # 1. Suma Ponderada (Z = X * W + B)
    z = np.dot(x, W) + B 
    
    # 2. Aplicar Activación
    salida = funcion_activacion(z)
    
    return salida, z

# --- 5. Ejecución y Resultados ---

print("=============================================")
print("  SIMULACIÓN DE NEURONA (Problema AND)")
print("=============================================")
print("Entradas (x1, x2) | Suma Ponderada (Z) | Salida (Predicción)")
print("-" * 50)

for x in X_prueba:
    salida, z = perceptron(x, W, B)
    
    # Formato para la salida
    salida_texto = "1 (VERDADERO)" if salida == 1 else "0 (FALSO)"
    
    print(f"  {x[0]}, {x[1]}             |     {z:.2f}             | {salida_texto}")