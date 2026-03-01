import numpy as np
import matplotlib.pyplot as plt

# --- A. Datos de Entrada (RGB, normalizados a [0, 1]) ---
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
RADIO_VECINDAD_INICIAL = max(TAMANO_MAPA) / 2 

# --- C. Inicialización de Pesos del Mapa ---
pesos_mapa = np.random.rand(TAMANO_MAPA[0], TAMANO_MAPA[1], DIM_PESOS)

# Guardar las coordenadas de cada neurona en el mapa para visualización
neurona_coords = np.array([[r, c] for r in range(TAMANO_MAPA[0]) for c in range(TAMANO_MAPA[1])])

def distancia_euclidiana(w, x):
    return np.sqrt(np.sum((w - x)**2, axis=-1))

def encontrar_bmu(x, pesos_mapa):
    distancias = distancia_euclidiana(pesos_mapa, x)
    return np.unravel_index(np.argmin(distancias), distancias.shape)

def funcion_vecindad(coord_neurona, coord_bmu, radio_vecindad):
    dist_fisica_al_bmu = np.sum((coord_neurona - coord_bmu)**2)
    return np.exp(-dist_fisica_al_bmu / (2 * (radio_vecindad**2)))

print("Iniciando entrenamiento del SOM...")

for epoch in range(EPOCHS):
    t = epoch + 1
    tasa_aprendizaje = TASA_APRENDIZAJE_INICIAL * np.exp(-t / EPOCHS)
    radio_vecindad = RADIO_VECINDAD_INICIAL * np.exp(-t / EPOCHS)
    
    for i in np.random.permutation(N_DATOS):
        x = colores_rgb[i]
        bmu_coord = encontrar_bmu(x, pesos_mapa)
        
        for r in range(TAMANO_MAPA[0]):
            for c in range(TAMANO_MAPA[1]):
                coord_neurona = np.array([r, c])
                influencia = funcion_vecindad(coord_neurona, bmu_coord, radio_vecindad)
                ajuste = tasa_aprendizaje * influencia * (x - pesos_mapa[r, c])
                pesos_mapa[r, c] += ajuste

# --- 4. Visualización de Resultados (Dos Gráficos) ---

plt.figure(figsize=(12, 6))

# --- GRÁFICO 1: Mapa Final de Colores ---
plt.subplot(1, 2, 1)
plt.imshow(pesos_mapa)
plt.title(f"Mapa Final de Colores del SOM ({TAMANO_MAPA[0]}x{TAMANO_MAPA[1]})")
plt.xlabel("Columna (0 a 2)")
plt.ylabel("Fila (0 a 1)")

# --- GRÁFICO 2: Puntos Originales y Asignación a BMU ---
plt.subplot(1, 2, 2)
plt.title("Asignación de Puntos Originales a BMU")
plt.xlabel("Coordenada X del Mapa")
plt.ylabel("Coordenada Y del Mapa")
plt.grid(True, linestyle=':', alpha=0.6)

# Graficar las neuronas del mapa como puntos, coloreadas por su peso RGB final
# Para simplificar, usamos las coordenadas de la neurona como su posición en el gráfico.
for r in range(TAMANO_MAPA[0]):
    for c in range(TAMANO_MAPA[1]):
        neuron_rgb = pesos_mapa[r, c]
        # Asegurarse de que los valores RGB estén en el rango correcto para el color
        plt.scatter(c, r, s=500, c=[neuron_rgb], marker='s', edgecolors='black', linewidth=1)
        plt.text(c, r, f'({r},{c})', ha='center', va='center', color='white' if np.mean(neuron_rgb) < 0.5 else 'black')

# Para cada dato de entrada, encontrar su BMU y dibujar una línea
for i, x_data in enumerate(colores_rgb):
    bmu_r, bmu_c = encontrar_bmu(x_data, pesos_mapa)
    
    # Colorear el punto original con su RGB real
    plt.scatter(bmu_c + (np.random.rand()-0.5)*0.2 , bmu_r + (np.random.rand()-0.5)*0.2, 
                s=150, c=[x_data], marker='o', edgecolors='grey', linewidth=0.5)
    
    # Dibujar una línea desde el punto de dato original a su BMU
    # (El offset aleatorio es para evitar que todos los puntos se superpongan exactamente)
    plt.plot([bmu_c + (np.random.rand()-0.5)*0.2, bmu_c], [bmu_r + (np.random.rand()-0.5)*0.2, bmu_r], 
             'k--', alpha=0.3, linewidth=0.5)
    
    plt.text(bmu_c + (np.random.rand()-0.5)*0.2 + 0.1, bmu_r + (np.random.rand()-0.5)*0.2 + 0.1, 
             colores_etiquetas[i], fontsize=8, color='black')

plt.xlim([-0.5, TAMANO_MAPA[1] - 0.5]) # Ajustar límites para que las neuronas se vean bien
plt.ylim([-0.5, TAMANO_MAPA[0] - 0.5])
plt.xticks(np.arange(TAMANO_MAPA[1]))
plt.yticks(np.arange(TAMANO_MAPA[0]))
plt.gca().invert_yaxis() # Poner el (0,0) arriba a la izquierda como en imshow
plt.tight_layout()
plt.show()

# Imprimir la clasificación final
print("\n--- Clasificación Final de los Colores ---")
for i, x in enumerate(colores_rgb):
    bmu_coord = encontrar_bmu(x, pesos_mapa)
    print(f"'{colores_etiquetas[i]}' ({x.round(1)}) -> Coordenada BMU: {bmu_coord}")