import numpy as np
import matplotlib.pyplot as plt

# --- A. Datos de Entrada (RGB, normalizados a [0, 1]) ---
# Queremos agrupar colores similares.
colores_etiquetas = ['Rojo', 'Verde', 'Azul', 'Cian', 'Magenta', 'Amarillo']
colores_rgb = np.array([
    [1.0, 0.0, 0.0],  # Rojo
    [0.0, 1.0, 0.0],  # Verde
    [0.0, 0.0, 1.0],  # Azul
    [0.0, 1.0, 1.0],  # Cian (G + B)
    [1.0, 0.0, 1.0],  # Magenta (R + B)
    [1.0, 1.0, 0.0]   # Amarillo (R + G)
])
N_DATOS = len(colores_rgb)

# --- B. Parámetros del Mapa ---
TAMANO_MAPA = (2, 3) # Cuadrícula de 2 filas x 3 columnas = 6 neuronas
DIM_PESOS = colores_rgb.shape[1] # 3 (RGB)
EPOCHS = 100 
TASA_APRENDIZAJE_INICIAL = 0.5
RADIO_VECINDAD_INICIAL = max(TAMANO_MAPA) / 2 # Radio inicial para la vecindad

# --- C. Inicialización de Pesos del Mapa ---
# Cada neurona (2x3=6) tiene un vector de pesos de dimensión 3 (RGB).
# Inicializamos los pesos con valores pequeños aleatorios.
pesos_mapa = np.random.rand(TAMANO_MAPA[0], TAMANO_MAPA[1], DIM_PESOS)

def distancia_euclidiana(w, x):
    """Calcula la distancia entre el peso w de la neurona y el vector de entrada x."""
    return np.sqrt(np.sum((w - x)**2, axis=-1))

def encontrar_bmu(x, pesos_mapa):
    """Encuentra la Unidad de Mejor Coincidencia (BMU)."""
    # Calcula la distancia de X a todos los pesos del mapa
    distancias = distancia_euclidiana(pesos_mapa, x)
    
    # Obtiene el índice (fila, col) de la distancia mínima
    return np.unravel_index(np.argmin(distancias), distancias.shape)

def funcion_vecindad(coord_neurona, coord_bmu, radio_vecindad):
    """
    Calcula el grado de influencia (fuerza de vecindad).
    Usamos la distancia euclidiana entre las coordenadas del mapa.
    """
    dist_fisica_al_bmu = np.sum((coord_neurona - coord_bmu)**2)
    return np.exp(-dist_fisica_al_bmu / (2 * (radio_vecindad**2)))

print("Iniciando entrenamiento del SOM...")

for epoch in range(EPOCHS):
    # Calcular la tasa de aprendizaje y el radio decrecientes
    t = epoch + 1
    tasa_aprendizaje = TASA_APRENDIZAJE_INICIAL * np.exp(-t / EPOCHS)
    radio_vecindad = RADIO_VECINDAD_INICIAL * np.exp(-t / EPOCHS)
    
    for i in np.random.permutation(N_DATOS): # Recorrer los datos aleatoriamente
        x = colores_rgb[i]
        
        # 1. Competencia: Encontrar la BMU
        bmu_coord = encontrar_bmu(x, pesos_mapa)
        
        # 2. Cooperación y Actualización
        for r in range(TAMANO_MAPA[0]):
            for c in range(TAMANO_MAPA[1]):
                coord_neurona = np.array([r, c])
                
                # a. Calcular la influencia de la vecindad
                influencia = funcion_vecindad(coord_neurona, bmu_coord, radio_vecindad)
                
                # b. Regla de Actualización de Pesos: W_nueva = W_antigua + alfa * influencia * (X - W_antigua)
                # Solo se ajustan las neuronas influenciadas
                ajuste = tasa_aprendizaje * influencia * (x - pesos_mapa[r, c])
                pesos_mapa[r, c] += ajuste

# --- 4. Visualización de Resultados ---

# Mostrar el mapa final: cada neurona tendrá un color final que representa el cluster.
plt.figure(figsize=(8, 6))
plt.imshow(pesos_mapa)
plt.title(f"Mapa Autoorganizado de Kohonen ({TAMANO_MAPA[0]}x{TAMANO_MAPA[1]})")
plt.xlabel("Columna (0 a 2)")
plt.ylabel("Fila (0 a 1)")

# Mapear los datos originales al mapa para ver la clasificación final
print("\n--- Clasificación Final de los Colores ---")
for i, x in enumerate(colores_rgb):
    bmu_coord = encontrar_bmu(x, pesos_mapa)
    print(f"'{colores_etiquetas[i]}' ({x.round(1)}) -> Coordenada BMU: {bmu_coord}")

plt.show()