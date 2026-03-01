import cv2
import numpy as np

# --- 1. Inicialización de la Captura de Video ---
# Cambia '0' por la ruta de un archivo de video (ej: 'video_prueba.mp4')
# si no quieres usar la cámara web.
captura = cv2.VideoCapture(0)

# Verificar que la cámara/video se abrió correctamente
if not captura.isOpened():
    print("Error: No se pudo abrir la fuente de video.")
    exit()

# Inicializar la variable que guardará el 'fondo'
fondo_estatico = None
area_minima_movimiento = 500  # Área mínima del contorno para considerarlo movimiento

print("Detector de Movimiento iniciado. Presiona 'q' para salir.")

# --- 2. Bucle Principal de Procesamiento de Frames ---
while True:
    # Capturar el frame actual
    ret, frame_actual = captura.read()

    if not ret:
        break  # Si no se pudo leer el frame, sal del bucle

    # Redimensionar (opcional, ayuda al rendimiento)
    frame_actual = cv2.resize(frame_actual, (500, 300))

    # 3. Preprocesamiento: Simplificar la imagen
    # Convertir a escala de grises
    frame_gris = cv2.cvtColor(frame_actual, cv2.COLOR_BGR2GRAY)

    # Aplicar desenfoque Gaussiano: Elimina el ruido fino para tener una mejor detección de bordes
    frame_gris_suavizado = cv2.GaussianBlur(frame_gris, (21, 21), 0)

    # 4. Inicializar el Fondo Estático
    # Si es la primera iteración, el fondo es el frame actual
    if fondo_estatico is None:
        fondo_estatico = frame_gris_suavizado
        continue  # Pasa al siguiente frame

    # 5. Resta de Frames (El corazón del detector de movimiento)
    # Calcular la diferencia absoluta entre el fondo y el frame actual
    resta_frames = cv2.absdiff(fondo_estatico, frame_gris_suavizado)

    # 6. Umbralización (Aislamiento del Movimiento)
    # Convertir la resta en una imagen binaria. Todo lo que sea "diferente"
    # (más de 25 píxeles de diferencia) se vuelve blanco (255).
    _, umbral = cv2.threshold(resta_frames, 25, 255, cv2.THRESH_BINARY)

    # 7. Dilatación (Relleno de agujeros)
    # Rellena los pequeños agujeros en los objetos en movimiento para hacerlos más sólidos.
    umbral_dilatado = cv2.dilate(umbral, None, iterations=2)

    # 8. Detección de Contornos
    # Encuentra los contornos (bordes) en la imagen umbralizada y dilatada.
    contornos, _ = cv2.findContours(umbral_dilatado.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 9. Filtrado y Dibujado de Rectángulos
    for contorno in contornos:
        # Filtrar contornos muy pequeños (ruido)
        if cv2.contourArea(contorno) < area_minima_movimiento:
            continue

        # Obtener las coordenadas del rectángulo que encierra el movimiento
        (x, y, w, h) = cv2.boundingRect(contorno)

        # Dibujar el rectángulo en el frame original a color
        cv2.rectangle(frame_actual, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame_actual, "Movimiento Detectado", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 10. Mostrar los resultados
    cv2.imshow("Original con Deteccion", frame_actual)
    cv2.imshow("Resta y Umbral (Movimiento aislado)", umbral_dilatado)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- 3. Liberación de Recursos ---
captura.release()
cv2.destroyAllWindows()