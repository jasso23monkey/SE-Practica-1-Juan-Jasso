import numpy as np

# --- 1. Rectified Linear Unit (ReLU) ---
def relu(x):
    # La salida es x si x > 0, de lo contrario es 0.
    return np.maximum(0, x)

def derivada_relu(x):
    # La derivada es 1 si x > 0, de lo contrario es 0.
    return np.where(x > 0, 1, 0)

# --- 2. Sigmoide (Usada en la capa de salida para clasificación binaria) ---
def sigmoide(x):
    return 1 / (1 + np.exp(-x))

def derivada_sigmoide(x):
    s = sigmoide(x)
    return s * (1 - s)

# --- 3. Tangente Hiperbólica (Tanh) ---
def tanh(x):
    return np.tanh(x)

def derivada_tanh(x):
    # La derivada es 1 - tanh(x)^2
    return 1 - np.tanh(x)**2

# --- PRUEBA ---
x_valores = np.array([-2.0, 0.0, 3.0])

print("====================================")
print("  FUNCIONES DE ACTIVACIÓN")
print("====================================")
print(f"Entradas X: {x_valores}")
print(f"ReLU(X):       {relu(x_valores)}")
print(f"Sigmoide(X):   {sigmoide(x_valores)}")
print(f"Tanh(X):       {tanh(x_valores)}")