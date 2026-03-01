import cv2
import numpy as np
import sys

imagen = cv2.imread("02_Probabilidad/07_Percepcion/paisaje.jpg")
# ¡DIAGNÓSTICO CRUCIAL!
if imagen is None:
    print("\n----------------------------------------------------")
    print("FALLO: La imagen no fue cargada.")
    print("CAUSA POSIBLE: El archivo 'paisaje.jpg' NO está en el directorio:")
    print("d:/IA-Juan-Jasso/02_Probabilidad/07_Percepción/")
    print("----------------------------------------------------")
    sys.exit(1) # Si falla la carga, detenemos el programa
else:
    # Si llega aquí, la carga fue exitosa.
    print(f"\nÉXITO: Imagen cargada correctamente. Forma: {imagen.shape}")


# 1. Aplicar un Filtro Gaussiano (Suavizado)
# Kernel de 5x5 y desviación estándar de 0
imagen_suavizada_gauss = cv2.GaussianBlur(imagen, (5, 5), 0)

# 2. Aplicar un Filtro Mediana (Eliminación de ruido impulsivo)
# Kernel de 5x5
imagen_suavizada_mediana = cv2.medianBlur(imagen, 5)

# 3. Aplicar un Filtro de Realce (Laplaciano)
# Se necesita una imagen de un solo canal (gris) para el Laplaciano
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
laplaciano = cv2.Laplacian(gris, cv2.CV_64F)
imagen_realzada = np.uint8(np.clip(gris + laplaciano, 0, 255)) # Combinar para realzar

print("Preprocesado: Aplicación de diferentes filtros con OpenCV:")
print("- Imagen Original (Ruidosa)")
print(f"- Filtro Gaussiano aplicado. Forma: {imagen_suavizada_gauss.shape}")
print(f"- Filtro Mediana aplicado. Forma: {imagen_suavizada_mediana.shape}")
print(f"- Imagen Realzada (Laplaciano) aplicada. Forma: {imagen_realzada.shape}")

# Para visualización (requiere cv2.imshow en un entorno gráfico)
cv2.imshow("Original", imagen)
cv2.imshow("Gaussiano", imagen_suavizada_gauss)
cv2.imshow("Mediana", imagen_suavizada_mediana)
cv2.imshow("Realzada", imagen_realzada)
cv2.waitKey(0)
cv2.destroyAllWindows()