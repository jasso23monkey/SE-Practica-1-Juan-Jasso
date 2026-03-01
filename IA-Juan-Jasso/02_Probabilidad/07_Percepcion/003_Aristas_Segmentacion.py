import cv2
import numpy as np

# ASUMIMOS QUE LA IMAGEN YA FUE CARGADA CON ÉXITO
# Aquí se usa una imagen de prueba simple para asegurar la ejecución
# En tu código, simplemente usa la variable 'imagen' ya cargada.
try:
    imagen_color = cv2.imread("paisaje.jpg") 
    if imagen_color is None:
        raise FileNotFoundError
except FileNotFoundError:
    # Crear una imagen de prueba si no se pudo cargar la real
    imagen_color = np.zeros((200, 200, 3), dtype=np.uint8)
    cv2.circle(imagen_color, (70, 100), 50, (255, 0, 0), -1)   # Círculo Azul
    cv2.circle(imagen_color, (130, 100), 50, (0, 0, 255), -1)  # Círculo Rojo
    cv2.circle(imagen_color, (100, 100), 30, (0, 255, 0), -1)  # Círculo Verde (se solapa)
    

# ----------------------------------------------------
# A. Detección de Bordes Canny (Para Contexto)
# ----------------------------------------------------
gris = cv2.cvtColor(imagen_color, cv2.COLOR_BGR2GRAY)
suavizada = cv2.GaussianBlur(gris, (5, 5), 0)
aristas_canny = cv2.Canny(suavizada, 50, 150)
print(f"Bordes Canny detectados. Forma: {aristas_canny.shape}")


# ----------------------------------------------------
# B. Segmentación (Watershed - Cuenca Hidrográfica)
# ----------------------------------------------------

# PASO 1: Umbralización para obtener el fondo y el objeto principal
# Convertir a binario (fondo negro, objetos blancos)
_, umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# PASO 2: Reducción de ruido morfológica
# Elimina los puntos blancos pequeños (ruido)
kernel = np.ones((3, 3), np.uint8)
apertura = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel, iterations=2)

# PASO 3: Definir la región de fondo (bg) y la región de primer plano (fg)
# El fondo seguro: dilatar la región abierta
fondo_seguro = cv2.dilate(apertura, kernel, iterations=3)

# El primer plano seguro (foreground): calcular la transformada de distancia
# Los píxeles muy lejos del fondo son el objeto seguro.
dist_transform = cv2.distanceTransform(apertura, cv2.DIST_L2, 5)
_, primer_plano_seguro = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
primer_plano_seguro = np.uint8(primer_plano_seguro)

# PASO 4: Crear los marcadores (markers)
# Los marcadores son la semilla que usará el algoritmo Watershed para crecer las regiones.
desconocido = cv2.subtract(fondo_seguro, primer_plano_seguro)

# Etiquetar los objetos (segmentos) de manera única
_, marcadores = cv2.connectedComponents(primer_plano_seguro)

# Sumar 1 a todos los marcadores para que el fondo no sea 0
marcadores = marcadores + 1

# Poner la región 'desconocida' (la cresta) en 0. Esta será la frontera.
marcadores[desconocido == 255] = 0

# PASO 5: Aplicar el algoritmo Watershed
marcadores = cv2.watershed(imagen_color, marcadores)

# PASO 6: Visualizar los resultados de la segmentación
# Dibujar la frontera entre los objetos segmentados en color rojo
imagen_segmentada = imagen_color.copy()
imagen_segmentada[marcadores == -1] = [0, 0, 255] # La frontera es -1 (rojo)


# ----------------------------------------------------
# Visualización
# ----------------------------------------------------

cv2.imshow("1 - Aristas (Canny)", aristas_canny)
cv2.imshow("2 - Segmentacion (Watershed)", imagen_segmentada)

print(f"Segmentación Watershed aplicada. Las fronteras segmentadas se marcan en rojo.")
cv2.waitKey(0)
cv2.destroyAllWindows()