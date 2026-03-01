import cv2
import numpy as np
import math

# --- 1. DEFINICIÓN DEL ESCENARIO ---
# Crear un lienzo (canvas) en blanco: 400x400 píxeles, 3 canales (BGR)
CANVAS_SIZE = 400
imagen = np.full((CANVAS_SIZE, CANVAS_SIZE, 3), 255, dtype=np.uint8) # 255 = Blanco

# Centro del lienzo (para centrar el objeto y las rotaciones)
CENTER = CANVAS_SIZE // 2

# --- 2. MODELADO: Vértices de un Triángulo 2D ---
# Coordenadas (x, y) relativas al centro del mundo (0,0)
# Las coordenadas en gráficos por computador usan (x, y) donde y crece hacia arriba.
# Aquí usamos el formato de matriz (y, x) con origen en la esquina superior izquierda.

# Definimos los vértices de un triángulo equilátero.
# Formato: (x, y)
vertices_originales = np.array([
    [0, -50],    # Punta superior
    [-50, 50],   # Esquina inferior izquierda
    [50, 50]     # Esquina inferior derecha
], dtype=np.float32)

# --- 3. TRANSFORMACIÓN: Rotación del Objeto ---

# Ángulo de rotación (30 grados)
ANGULO_GRADOS = 30
angulo_radianes = math.radians(ANGULO_GRADOS)

# Matriz de Rotación 2D: [cos(a) -sin(a)]
#                       [sin(a)  cos(a)]
matriz_rotacion = np.array([
    [math.cos(angulo_radianes), -math.sin(angulo_radianes)],
    [math.sin(angulo_radianes), math.cos(angulo_radianes)]
])

# Aplicar la rotación a los vértices
vertices_rotados = np.dot(vertices_originales, matriz_rotacion)

# --- 4. PROYECCIÓN Y RASTERIZADO (Dibujo en Pantalla) ---

# Ajustar los vértices rotados al sistema de coordenadas de la imagen (de [-200, 200] a [0, 400])
# 1. Aplicar Traslación: Añadir el centro del lienzo a las coordenadas (x, y)
# 2. Invertir el eje Y: En imágenes, Y crece hacia abajo. Se invierte solo el eje Y proyectado.
vertices_finales_cv = []
for x_rot, y_rot in vertices_rotados:
    # Trasladar el punto al centro de la imagen y corregir la orientación Y
    x_pantalla = int(x_rot + CENTER)
    y_pantalla = int(CENTER - y_rot)  # Restamos para que el Y positivo vaya hacia arriba
    vertices_finales_cv.append([x_pantalla, y_pantalla])

# Convertir a formato que acepta cv2.polylines (Array de enteros)
puntos = np.array(vertices_finales_cv, dtype=np.int32).reshape((-1, 1, 2))

# RASTERIZAR: Dibujar el polígono transformado en el lienzo
# cv2.polylines dibuja los límites, simulando la etapa final de renderizado.
cv2.polylines(imagen, [puntos], isClosed=True, color=(0, 0, 0), thickness=2) # Negro

# Añadir etiquetas de texto
cv2.putText(imagen, f"Rotado {ANGULO_GRADOS} grados", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
#cv2.putText(imagen, "Elaborado con OpenCV y NumPy", (10, CANVAS_SIZE - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 150), 1)


# --- 5. VISUALIZACIÓN ---
# La función imshow de OpenCV requiere un entorno gráfico (PyCharm, VS Code con extensiones)
try:
    cv2.imshow("Graficos por Computador: Triangulo Rotado", imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
except cv2.error as e:
    print("\n--- ERROR DE VISUALIZACIÓN ---")
    print("No se pudo mostrar la imagen con cv2.imshow().")
    print("Asegúrate de estar en un entorno que soporte visualización gráfica (PyCharm o VS Code con el entorno configurado).")
    print("Guardando imagen como 'triangulo_rotado.png' para revisión.")
    cv2.imwrite("triangulo_rotado.png", imagen)