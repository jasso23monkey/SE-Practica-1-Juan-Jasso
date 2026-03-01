import cv2
import numpy as np

# Leer la imagen
imagen = cv2.imread("02_Probabilidad/07_Percepcion/monedas.jpeg")
if imagen is None:
    print("No se encontró la imagen.")
    exit()

# Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gris, (9, 9), 0)
_, binaria = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

contornos, jerarquia = cv2.findContours(binaria, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
salida = imagen.copy()
cv2.drawContours(salida, contornos, -1, (0, 255, 0), 2)

num_monedas = len(contornos)
texto = f"Monedas detectadas: {num_monedas}"
cv2.putText(salida, texto, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

cv2.imshow('Original', imagen)
cv2.imshow('Binaria', binaria)
cv2.imshow('Detección de Monedas', salida)

cv2.waitKey(0)
cv2.destroyAllWindows()