import cv2
import numpy as np
import sys

# --- CONFIGURACIÓN DE RUTAS ---
# Usa una imagen de un documento, texto impreso o texto limpio para mejores resultados.
RUTA_IMAGEN = "documento.png" 

# --- 1. CARGAR IMAGEN Y PREPROCESAMIENTO ---
try:
    imagen_original = cv2.imread(RUTA_IMAGEN)
    if imagen_original is None:
        # Crea una imagen de prueba simple si no se encuentra el archivo
        imagen_original = np.zeros((150, 400, 3), dtype=np.uint8)
        cv2.putText(imagen_original, "HOLA PRUEBA", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
        print("\nADVERTENCIA: Usando imagen de texto generada. Los resultados de segmentación serán muy limpios.")
        
except Exception:
    print("Error al cargar la imagen. Saliendo.")
    sys.exit(1)

# Convertir a escala de grises
gris = cv2.cvtColor(imagen_original, cv2.COLOR_BGR2GRAY)

# Binarización (Umbralización OTSU)
# Separa el texto (negro) del fondo (blanco) para un mejor análisis de contornos
_, binarizada = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# --- 2. ELIMINACIÓN DE RUIDO MORFOLÓGICO (Opcional, pero útil) ---
# Elimina pequeños puntos de ruido que pueden detectarse como contornos.
kernel = np.ones((2, 2), np.uint8)
limpieza = cv2.morphologyEx(binarizada, cv2.MORPH_OPEN, kernel, iterations=1)


# --- 3. SEGMENTACIÓN: Detección de Contornos (Cada Contorno = Un Carácter) ---

# cv2.findContours encuentra las fronteras de los objetos blancos (nuestro texto).
# RETR_EXTERNAL: Recupera solo los contornos externos (para las palabras/letras).
# CHAIN_APPROX_SIMPLE: Comprime los puntos innecesarios.
contornos, _ = cv2.findContours(limpieza, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Copia de la imagen original para dibujar los resultados
imagen_segmentada = imagen_original.copy()

caracteres_segmentados = 0
for cnt in contornos:
    # Filtro: Ignorar contornos muy pequeños (considerados ruido)
    if cv2.contourArea(cnt) > 100:
        # Obtener el rectángulo delimitador (Bounding Box) alrededor del contorno
        (x, y, w, h) = cv2.boundingRect(cnt)
        
        # Dibujar un rectángulo alrededor del carácter detectado
        cv2.rectangle(imagen_segmentada, (x, y), (x + w, y + h), (0, 255, 0), 2) # Verde
        
        caracteres_segmentados += 1

# --- 4. VISUALIZACIÓN ---
print("\n=================================================")
print(" SIMULACIÓN DE SEGMENTACIÓN OCR (Solo OpenCV)")
print("=================================================")
print(f"Total de posibles caracteres/componentes segmentados: {caracteres_segmentados}")
print("Las cajas verdes representan los caracteres segmentados listos para la CLASIFICACIÓN (que requeriría Tesseract o un modelo ML).")

cv2.imshow("0 - Binarizada y Limpia", limpieza)
cv2.imshow("1 - Segmentacion de Caracteres", imagen_segmentada)
cv2.waitKey(0)
cv2.destroyAllWindows()