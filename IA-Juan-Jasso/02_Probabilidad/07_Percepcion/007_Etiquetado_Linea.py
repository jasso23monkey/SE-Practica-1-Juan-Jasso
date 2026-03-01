import cv2
import numpy as np
import sys

# --- CONFIGURACIÓN DE RUTAS ---
# Usaremos la carpeta sin el acento
RUTA_IMAGEN = "02_Probabilidad/07_Percepcion/paisaje.jpg" 

# --- 1. CARGAR IMAGEN Y PREPROCESAMIENTO ---
imagen_original = cv2.imread(RUTA_IMAGEN)
if imagen_original is None:
    print("¡ERROR FATAL! No se pudo cargar la imagen.")
    sys.exit(1)

alto, ancho, _ = imagen_original.shape
imagen_lineas = imagen_original.copy()

# Convertir a escala de grises y suavizar (Pre-requisito para Canny)
gris = cv2.cvtColor(imagen_original, cv2.COLOR_BGR2GRAY)
suavizada = cv2.GaussianBlur(gris, (5, 5), 0)

# Detección de Aristas Canny (Entrada a la Transformada de Hough)
aristas = cv2.Canny(suavizada, 50, 150)

# --- 2. DETECCIÓN DE LÍNEAS (Transformada de Hough Probabilística) ---
# HoughLinesP es más eficiente que HoughLines porque solo devuelve los puntos finales de las líneas.
# Parámetros:
# aristas: Imagen binaria de entrada (de Canny).
# 1: Resolución de rho (1 píxel).
# np.pi/180: Resolución de theta (1 grado).
# 100: Umbral (mínimo de intersecciones en el acumulador para considerar una línea).
# 10: Longitud mínima de la línea a detectar.
# 5: Distancia máxima permitida entre segmentos de línea para unirlos.

lineas = cv2.HoughLinesP(aristas, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)


# --- 3. ETIQUETADO Y DIBUJO ---
if lineas is not None:
    print(f"\nTotal de líneas detectadas: {len(lineas)}")
    
    for i, line in enumerate(lineas):
        # La línea es devuelta como 4 coordenadas: (x1, y1, x2, y2)
        x1, y1, x2, y2 = line[0]
        
        # Etiquetado simple: asignar un color para la visualización.
        # En una aplicación real, se calcularía el ángulo para etiquetar como "Horizontal" o "Vertical".
        
        # Dibujar la línea sobre la copia de la imagen
        cv2.line(imagen_lineas, (x1, y1), (x2, y2), (0, 255, 0), 2) # Verde
        
        # Etiquetado: Dibujar el índice de la línea para su identificación
        cv2.putText(imagen_lineas, str(i + 1), (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

# --- 4. VISUALIZACIÓN ---
cv2.imshow("0 - Aristas (Canny)", aristas)
cv2.imshow("1 - Etiquetado de Lineas (Hough)", imagen_lineas)
print("\nPresiona cualquier tecla para cerrar las ventanas.")
cv2.waitKey(0)
cv2.destroyAllWindows()