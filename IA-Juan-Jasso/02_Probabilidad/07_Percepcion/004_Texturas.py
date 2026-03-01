import cv2
import numpy as np
import sys

# --- CONFIGURACIÓN DE RUTAS Y PARÁMETROS ---
RUTA_IMAGEN = "02_Probabilidad/07_Percepcion/paisaje.jpg"
FACTOR_TEXTURA = 0.3 # Ajusta la intensidad de la textura (0.0 a 1.0)

# --- 1. CARGAR IMAGEN Y GESTIONAR ERRORES ---
imagen_original = cv2.imread(RUTA_IMAGEN)

if imagen_original is None:
    print("\n----------------------------------------------------")
    print("¡ERROR FATAL! No se pudo cargar la imagen 'paisaje.jpg'.")
    print(f"Verifica la ruta: {RUTA_IMAGEN}")
    print("----------------------------------------------------")
    sys.exit(1)
else:
    print(f"\nÉXITO: Imagen original cargada correctamente. Forma: {imagen_original.shape}")

# Obtener dimensiones de la imagen original
alto, ancho, _ = imagen_original.shape

# --- 2. GENERAR TEXTURA DIAGONAL ---
# Creamos una imagen de textura del mismo tamaño que la original.
textura_diagonal = np.zeros((alto, ancho), dtype=np.uint8)
intensidad_claro = 200 # Valor de pixel para las rayas claras
intensidad_oscuro = 50  # Valor de pixel para las rayas oscuras
espaciado = 20        # Ajusta el ancho de las rayas

for y in range(alto):
    for x in range(ancho):
        # Crear un patrón de rayas diagonales (cambiar espaciado para grosor)
        if (x + y) % espaciado < espaciado // 2:
            textura_diagonal[y, x] = intensidad_claro
        else:
            textura_diagonal[y, x] = intensidad_oscuro

# Convertir la textura a 3 canales para poder fusionarla con la imagen a color
textura_diagonal_color = cv2.cvtColor(textura_diagonal, cv2.COLOR_GRAY2BGR)

# --- 3. SUPERPONER TEXTURA EN LA IMAGEN ORIGINAL ---
# Usamos cv2.addWeighted para combinar las imágenes.
# La textura se superpone con una cierta transparencia (FACTOR_TEXTURA).
imagen_con_textura = cv2.addWeighted(imagen_original, 1 - FACTOR_TEXTURA, textura_diagonal_color, FACTOR_TEXTURA, 0)
print(f"Textura diagonal superpuesta con factor {FACTOR_TEXTURA:.1f}.")

# --- 4. ACENTUAR SOMBRAS (Realce de Contraste Adaptativo - CLAHE) ---
# Para acentuar sombras, la idea es aumentar el contraste en las regiones oscuras.
# CLAHE (Contrast Limited Adaptive Histogram Equalization) es excelente para esto.

# Primero, convertimos la imagen a un espacio de color que separe la luminancia (brillo) del color.
# El espacio LAB es ideal: L = Luminancia, A = Canal verde-rojo, B = Canal azul-amarillo.
lab = cv2.cvtColor(imagen_con_textura, cv2.COLOR_BGR2LAB)

# Separar el canal de luminancia
l_channel = lab[:, :, 0]

# Crear un objeto CLAHE
# clipLimit: Umbral para limitar el contraste (ej., 2.0). Más alto = más contraste.
# tileGridSize: Tamaño de la región para la ecualización local (ej., 8x8).
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

# Aplicar CLAHE al canal de luminancia
cl = clahe.apply(l_channel)

# Combinar el canal de luminancia realzado con los canales A y B originales
lab_realzado = np.zeros_like(lab)
lab_realzado[:, :, 0] = cl
lab_realzado[:, :, 1:] = lab[:, :, 1:] # Copiar A y B originales

# Convertir de nuevo al espacio de color BGR
imagen_con_sombras_acentuadas = cv2.cvtColor(lab_realzado, cv2.COLOR_LAB2BGR)
print("Sombras acentuadas (contraste local realzado con CLAHE).")


# --- 5. VISUALIZACIÓN DE RESULTADOS ---
cv2.imshow("0 - Imagen Original", imagen_original)
cv2.imshow("1 - Textura Diagonal Generada", textura_diagonal_color)
cv2.imshow("2 - Imagen con Textura Superpuesta", imagen_con_textura)
cv2.imshow("3 - Imagen con Textura y Sombras Acentuadas", imagen_con_sombras_acentuadas)

print("\nPresiona cualquier tecla para cerrar las ventanas.")
cv2.waitKey(0)
cv2.destroyAllWindows()