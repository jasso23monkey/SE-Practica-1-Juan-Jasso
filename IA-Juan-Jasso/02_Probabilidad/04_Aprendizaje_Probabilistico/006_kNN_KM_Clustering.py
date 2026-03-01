import numpy as np
import matplotlib.pyplot as plt

# --- A. Simulación de Datos (Flores por tamaño y color) ---
np.random.seed(42)
N_PUNTOS = 150
K_MEDIAS = 3 # Queremos 3 grupos/especies

# Generar 3 grupos simulados (Características: Largo_Petalo, Ancho_Petalo)
datos_g1 = np.random.normal(loc=[2, 0.5], scale=0.3, size=(50, 2))
datos_g2 = np.random.normal(loc=[5, 1.5], scale=0.4, size=(50, 2))
datos_g3 = np.random.normal(loc=[7, 2.5], scale=0.5, size=(50, 2))

# Conjunto de datos X (sin etiquetas iniciales)
X = np.vstack([datos_g1, datos_g2, datos_g3])
N_TOTAL = len(X)

# --- B. Implementación del Algoritmo k-Medias (Clustering) ---

# 1. Inicialización de Centroides
indices_iniciales = np.random.choice(N_TOTAL, K_MEDIAS, replace=False)
centroides = X[indices_iniciales]
etiquetas_cluster = np.zeros(N_TOTAL, dtype=int)
MAX_ITER = 10

# Función de Distancia (Euclidiana)
def distancia_euclidiana(punto, centroides):
    return np.sqrt(np.sum((punto - centroides) ** 2, axis=1))

# Bucle de k-Medias
for iteracion in range(MAX_ITER):
    centroides_antiguos = centroides.copy()
    
    # Asignación (E-Step)
    for i in range(N_TOTAL):
        distancias = distancia_euclidiana(X[i], centroides)
        etiquetas_cluster[i] = np.argmin(distancias)

    # Actualización (M-Step)
    nuevo_centroides = np.zeros((K_MEDIAS, X.shape[1]))
    for k in range(K_MEDIAS):
        puntos_cluster_k = X[etiquetas_cluster == k]
        if len(puntos_cluster_k) > 0:
            nuevo_centroides[k] = np.mean(puntos_cluster_k, axis=0)
        else:
            nuevo_centroides[k] = centroides_antiguos[k]

    centroides = nuevo_centroides
    
    # Detener si converge
    if np.sum((centroides - centroides_antiguos)**2) < 1e-4:
        break

print(f"K-Medias finalizó en {iteracion + 1} iteraciones.")
print("Las etiquetas del cluster (0, 1, 2) son ahora nuestras 'etiquetas' de entrenamiento.")

# --- C. Implementación del Algoritmo k-NN (Clasificación) ---

# Nuevo punto de datos (Flor desconocida)
NUEVO_PUNTO = np.array([5.5, 1.8]) # Una flor nueva, cerca del grupo 2
K_NN = 5 # Número de vecinos a considerar

def clasificar_k_nn(punto_nuevo, X_entrenamiento, etiquetas_entrenamiento, k):
    """Clasifica un nuevo punto usando k-NN."""
    distancias = np.zeros(len(X_entrenamiento))
    
    # 1. Calcular Distancias a todos los puntos de entrenamiento
    for i in range(len(X_entrenamiento)):
        distancias[i] = np.linalg.norm(punto_nuevo - X_entrenamiento[i])
    
    # 2. Obtener los índices de los K vecinos más cercanos
    indices_k_cercanos = np.argsort(distancias)[:k]
    
    # 3. Obtener las etiquetas de esos K vecinos
    etiquetas_k_cercanos = etiquetas_entrenamiento[indices_k_cercanos]
    
    # 4. Encontrar la clase más común (voto mayoritario)
    # np.bincount cuenta ocurrencias de enteros.
    votos = np.bincount(etiquetas_k_cercanos)
    clase_predicha = np.argmax(votos)
    
    return clase_predicha, indices_k_cercanos

# Ejecutar k-NN usando las etiquetas creadas por k-Medias
clase_predicha, indices_k_cercanos = clasificar_k_nn(NUEVO_PUNTO, X, etiquetas_cluster, K_NN)

# --- D. Visualización de los Resultados ---

plt.figure(figsize=(10, 7))

# Colores y Marcadores
colores = np.array(['#1f77b4', '#ff7f0e', '#2ca02c']) # Azul, Naranja, Verde

# 1. Graficar los datos (Agrupamiento k-Medias)
plt.scatter(X[:, 0], X[:, 1], c=colores[etiquetas_cluster], 
            label='Datos Agrupados por k-Medias', alpha=0.6, s=50)

# 2. Graficar los Centroides
plt.scatter(centroides[:, 0], centroides[:, 1], 
            marker='X', s=200, c='black', label='Centroides (k-Medias)', edgecolors='white', linewidth=2)

# 3. Graficar el Nuevo Punto y sus Vecinos (k-NN)
plt.scatter(NUEVO_PUNTO[0], NUEVO_PUNTO[1], marker='*', s=300, c='red', 
            label=f'Nuevo Punto (Predicción: Cluster {clase_predicha})', edgecolors='black', linewidth=1.5, zorder=3)

# Resaltar los K vecinos más cercanos
plt.scatter(X[indices_k_cercanos, 0], X[indices_k_cercanos, 1], 
            marker='o', s=350, facecolors='none', edgecolors='red', linewidth=1.5, label=f'{K_NN} Vecinos (k-NN)')


plt.title('Integración de K-Medias (Clustering) y k-NN (Clasificación)')
plt.xlabel('Característica: Largo del Pétalo')
plt.ylabel('Característica: Ancho del Pétalo')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.5)
plt.show()

print("\n=============================================")
print("  RESULTADO DE LA CLASIFICACIÓN (k-NN) ")
print("=============================================")
print(f"El Nuevo Punto ([{NUEVO_PUNTO[0]}, {NUEVO_PUNTO[1]}]) ha sido:")
print(f"Predicho para la Clase (Cluster): {clase_predicha}")