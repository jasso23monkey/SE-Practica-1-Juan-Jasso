import numpy as np
import matplotlib.pyplot as plt

# --- A. Simulación de Datos (3 Clusters Distintos) ---
np.random.seed(42)
N_PUNTOS = 300
K = 3 # Queremos encontrar 3 clusters

# Generar 3 grupos sintéticos alrededor de diferentes centros
datos_cluster1 = np.random.normal(loc=[0, 1], scale=0.5, size=(100, 2))
datos_cluster2 = np.random.normal(loc=[5, 7], scale=0.8, size=(100, 2))
datos_cluster3 = np.random.normal(loc=[-1, 8], scale=0.6, size=(100, 2))

# Conjunto de datos completo
X = np.vstack([datos_cluster1, datos_cluster2, datos_cluster3])
N_TOTAL = len(X)

# --- B. Inicialización ---

# Inicializar K centroides aleatoriamente seleccionando K puntos del dataset
indices_iniciales = np.random.choice(N_TOTAL, K, replace=False)
centroides = X[indices_iniciales]

MAX_ITER = 100
TOLERANCIA = 1e-4 # Criterio de parada para el movimiento del centroide
etiquetas = np.zeros(N_TOTAL, dtype=int) # Almacenará el índice del cluster asignado (0, 1, o 2)

# --- C. Función de Distancia Euclidiana ---
def calcular_distancia(punto, centroides):
    """Calcula la distancia Euclidiana de un punto a todos los centroides."""
    # NumPy permite restar el vector (punto) de la matriz de centroides
    return np.sqrt(np.sum((punto - centroides) ** 2, axis=1))

# --- D. Función de Distancia Euclidiana ---
def calcular_distancia_euclidiana(punto, centroides):
    """Calcula la distancia Euclidiana de un punto a todos los centroides."""
    # NumPy permite restar el vector (punto) de la matriz de centroides
    return np.sqrt(np.sum((punto - centroides) ** 2, axis=1))

historial_centroides = [centroides.copy()]

for iteracion in range(MAX_ITER):
    centroides_antiguos = centroides.copy()
    
    # =================================================================
    # PASO 1: ASIGNACIÓN (E-Step en el contexto del EM, aunque es K-Means)
    # Asignar cada punto al centroide más cercano.
    # =================================================================
    for i in range(N_TOTAL):
        # Calcular la distancia del punto X[i] a cada uno de los K centroides
        distancias = calcular_distancia_euclidiana(X[i], centroides)
        # La nueva etiqueta es el índice del centroide más cercano (el mínimo)
        etiquetas[i] = np.argmin(distancias)

    # =================================================================
    # PASO 2: ACTUALIZACIÓN (M-Step)
    # Recalcular los centroides al centro de sus puntos asignados.
    # =================================================================
    nuevo_centroides = np.zeros((K, X.shape[1]))
    movimiento_total = 0
    
    for k in range(K):
        # Encontrar todos los puntos asignados al cluster k
        puntos_cluster_k = X[etiquetas == k]
        
        if len(puntos_cluster_k) > 0:
            # Calcular la nueva media de esos puntos
            nuevo_centroides[k] = np.mean(puntos_cluster_k, axis=0)
        else:
            # Si un cluster está vacío, no mover el centroide
            nuevo_centroides[k] = centroides_antiguos[k]

        # Calcular el movimiento (para el criterio de parada)
        movimiento_total += np.sum((nuevo_centroides[k] - centroides_antiguos[k])**2)
    
    centroides = nuevo_centroides
    historial_centroides.append(centroides.copy())

    # =================================================================
    # Verificación de Convergencia
    # =================================================================
    if movimiento_total < TOLERANCIA:
        print(f"K-Means convergió en la iteración {iteracion + 1}.")
        break

# --- 3. Visualización de los Resultados ---

plt.figure(figsize=(10, 7))

# Colores para los clusters
colores = ['blue', 'red', 'green'] 

# Graficar los puntos con el color de su cluster final
for k in range(K):
    puntos_cluster = X[etiquetas == k]
    plt.scatter(puntos_cluster[:, 0], puntos_cluster[:, 1], 
                c=colores[k], label=f'Cluster {k+1}', alpha=0.6, edgecolors='w', s=50)

# Graficar los centroides finales
plt.scatter(centroides[:, 0], centroides[:, 1], 
            marker='X', s=200, c='black', label='Centroides Finales', edgecolors='white', linewidth=2)

plt.title(f'Agrupamiento K-Means con K={K} (Convergió en {iteracion + 1} iteraciones)')
plt.xlabel('Característica 1')
plt.ylabel('Característica 2')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.5)
plt.show()