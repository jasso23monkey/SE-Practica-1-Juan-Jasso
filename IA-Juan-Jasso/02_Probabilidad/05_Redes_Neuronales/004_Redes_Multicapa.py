import numpy as np
import matplotlib.pyplot as plt

# --- A. Funciones de Activación ---
def tanh(x):
    """Tangente Hiperbólica (Tanh) - Rango [-1, 1], preferida sobre Sigmoide en capas ocultas."""
    return np.tanh(x)

def derivada_tanh(x):
    return 1 - np.tanh(x)**2

def sigmoide(x):
    """Sigmoide - Rango [0, 1], perfecta para la capa de salida de clasificación binaria."""
    return 1 / (1 + np.exp(-x))

# --- B. Generación de Datos de Círculo (Simulado) ---
np.random.seed(42)
N_MUESTRAS = 100

# Generar puntos: un círculo interno (Clase 0) y un anillo externo (Clase 1)
def make_circles_data(n_muestras):
    radio_externo = np.linspace(1.0, 1.5, n_muestras // 2) + np.random.normal(0, 0.05, n_muestras // 2)
    radio_interno = np.linspace(0.0, 0.5, n_muestras // 2) + np.random.normal(0, 0.05, n_muestras // 2)
    
    angulos = np.random.uniform(0, 2 * np.pi, n_muestras)
    
    X = np.zeros((n_muestras, 2))
    Y = np.zeros((n_muestras, 1))

    # Clase 0 (Círculo interno)
    X[:n_muestras//2, 0] = radio_interno * np.cos(angulos[:n_muestras//2])
    X[:n_muestras//2, 1] = radio_interno * np.sin(angulos[:n_muestras//2])
    Y[:n_muestras//2] = 0

    # Clase 1 (Anillo externo)
    X[n_muestras//2:, 0] = radio_externo * np.cos(angulos[n_muestras//2:])
    X[n_muestras//2:, 1] = radio_externo * np.sin(angulos[n_muestras//2:])
    Y[n_muestras//2:] = 1
    
    return X, Y

X, Y = make_circles_data(N_MUESTRAS)

# --- C. Arquitectura y Parámetros ---
N_ENTRADA = 2
N_OCULTA_1 = 10   # Aumentamos las neuronas para la complejidad geométrica
N_SALIDA = 1
TASA_APRENDIZAJE = 0.05
EPOCHS = 20000

# Capa 1: Entrada (2) -> Oculta (10)
W1 = np.random.uniform(low=-0.5, high=0.5, size=(N_ENTRADA, N_OCULTA_1))
B1 = np.zeros((1, N_OCULTA_1))

# Capa 2: Oculta (10) -> Salida (1)
W2 = np.random.uniform(low=-0.5, high=0.5, size=(N_OCULTA_1, N_SALIDA))
B2 = np.zeros((1, N_SALIDA))

print("Iniciando entrenamiento para la Clasificación de Círculo...")
for i in range(EPOCHS):
    
    # --- Propagación Adelante (Forward Pass) ---
    # Capa Oculta (Usando Tanh)
    Z1 = np.dot(X, W1) + B1
    A1 = tanh(Z1)
    
    # Capa de Salida (Usando Sigmoide)
    Z2 = np.dot(A1, W2) + B2
    A2 = sigmoide(Z2) # Predicción final

    # --- Retropropagación del Error (Backpropagation) ---
    
    # 1. Error en la Salida
    error_salida = A2 - Y
    
    # 2. Delta de la Salida (Gradiente Capa 2)
    # D2 = E * Sigmoide'(Z2)
    D2 = error_salida * (A2 * (1 - A2)) # Derivada simplificada de Sigmoide
    
    # 3. Delta de la Capa Oculta (Gradiente Capa 1)
    # D1 = (D2 @ W2.T) * Tanh'(Z1)
    D1 = np.dot(D2, W2.T) * derivada_tanh(Z1)
    
    # --- Actualización de Pesos ---
    
    # Actualizar W2 y B2 (Capa de Salida)
    W2 -= TASA_APRENDIZAJE * np.dot(A1.T, D2)
    B2 -= TASA_APRENDIZAJE * np.sum(D2, axis=0, keepdims=True)
    
    # Actualizar W1 y B1 (Capa Oculta)
    W1 -= TASA_APRENDIZAJE * np.dot(X.T, D1)
    B1 -= TASA_APRENDIZAJE * np.sum(D1, axis=0, keepdims=True)
    
    if i % 2000 == 0:
        loss = np.mean(np.square(error_salida))
        print(f"Epoch {i}: Error (MSE) = {loss:.6f}")

# Función para dibujar la frontera de decisión aprendida
def plot_decision_boundary(pred_func, X, Y):
    # Definir la cuadrícula (grid) para evaluar la función
    x_min, x_max = X[:, 0].min() - 0.5, X[:, 0].max() + 0.5
    y_min, y_max = X[:, 1].min() - 0.5, X[:, 1].max() + 0.5
    h = 0.01
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    
    # Evaluar la red en todos los puntos del grid
    Z = pred_func(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # Dibujar el contorno y los puntos de datos
    plt.contourf(xx, yy, Z, cmap=plt.cm.Spectral, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=Y.flatten(), cmap=plt.cm.Spectral, edgecolors='k')
    plt.title("Frontera de Decisión de la Red Multicapa (MLP)")
    plt.xlabel("Característica 1")
    plt.ylabel("Característica 2")

# Función de predicción usando los pesos finales
def predict(X_in):
    # Forward pass usando los pesos entrenados
    Z1 = np.dot(X_in, W1) + B1
    A1 = tanh(Z1)
    Z2 = np.dot(A1, W2) + B2
    A2 = sigmoide(Z2)
    return np.round(A2)

# Graficar
plt.figure(figsize=(8, 6))
plot_decision_boundary(lambda x: predict(x), X, Y)
plt.show()

# Precisión de clasificación en los datos de entrenamiento
predicciones_finales = predict(X)
precision = np.mean(predicciones_finales.flatten() == Y.flatten())
print(f"\nPrecisión final en los datos de entrenamiento: {precision * 100:.2f}%")