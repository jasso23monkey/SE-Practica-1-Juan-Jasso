import cv2
import numpy as np
import sys

# --- CONFIGURACIÓN DE PUNTOS Y PARÁMETROS ---
# Parámetros para el detector de puntos (Shi-Tomasi)
feature_params = dict(maxCorners=100, qualityLevel=0.3, minDistance=7, blockSize=7)

# Parámetros para el Flujo Óptico Lucas-Kanade
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Color de las líneas de rastreo (Verde BGR)
color = (0, 255, 0)

# Inicializar un array para almacenar las líneas de rastreo (imagen de salida)
mask = None

# --- CARGAR LA IMAGEN Y SIMULAR EL PRIMER FRAME ---
# Para simular, se puede usar tu 'paisaje.jpg' dos veces
RUTA_IMAGEN = "02_Probabilidad/07_Percepcion/paisaje.jpg" 
imagen_base = cv2.imread(RUTA_IMAGEN)

if imagen_base is None:
    print("¡ERROR! No se pudo cargar la imagen para simular el movimiento.")
    sys.exit(1)

# Convertir a escala de grises
old_gray = cv2.cvtColor(imagen_base, cv2.COLOR_BGR2GRAY)
alto, ancho = old_gray.shape

# Encontrar los puntos característicos (puntos clave para rastrear) en el primer frame
p0 = cv2.goodFeaturesToTrack(old_gray, mask=None, **feature_params)

# Crear la máscara para dibujar el rastro
mask = np.zeros_like(imagen_base)

# --- SIMULACIÓN DEL SEGUNDO FRAME (MOVIMIENTO) ---
# En un video real, esto sería el siguiente frame (cap.read())
# Aquí, simulamos el movimiento trasladando el segundo frame virtualmente.

# Simular una traslación hacia la derecha y abajo
matriz_traslacion = np.float32([[1, 0, 10], [0, 1, 10]]) # Mueve 10px a X y 10px a Y

# Aplica la traslación al frame base (simulando el nuevo frame 'siguiente')
frame_next = cv2.warpAffine(imagen_base, matriz_traslacion, (ancho, alto))
frame_gray = cv2.cvtColor(frame_next, cv2.COLOR_BGR2GRAY)

# -------------------------------------------------------------------
# APLICACIÓN DEL ALGORITMO DE FLUJO ÓPTICO LUCAS-KANADE
# -------------------------------------------------------------------

# Calcula el Flujo Óptico
# p0: puntos del frame anterior
# p1: puntos rastreados en el frame actual
# st: estado (1 si el punto fue encontrado, 0 si no)
# err: error de rastreo
p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)

# Seleccionar los puntos encontrados (st == 1)
good_new = p1[st == 1]
good_old = p0[st == 1]

# --- DIBUJAR LOS VECTORES DE MOVIMIENTO (RASTREO) ---

for i, (new, old) in enumerate(zip(good_new, good_old)):
    a, b = new.ravel().astype(int) # Coordenadas nuevas
    c, d = old.ravel().astype(int) # Coordenadas antiguas

    # 1. Dibuja el rastro del movimiento (la línea)
    mask = cv2.line(mask, (a, b), (c, d), color, 2)
    
    # 2. Dibuja el punto rastreado en el frame actual
    frame_next = cv2.circle(frame_next, (a, b), 5, color, -1)

# Superponer el rastro (máscara) sobre el frame actual
img = cv2.add(frame_next, mask)

# --- VISUALIZACIÓN ---
cv2.imshow('Deteccion de Movimiento (Flujo Optico)', img)
print(f"Rastreo de {len(good_new)} puntos clave aplicado. La imagen simuló moverse 10px a la derecha y 10px hacia abajo.")
print("\nPresiona cualquier tecla para cerrar la ventana.")
cv2.waitKey(0)
cv2.destroyAllWindows()