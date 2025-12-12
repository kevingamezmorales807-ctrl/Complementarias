# 📦 Importar librerías necesarias
import cv2              # OpenCV: librería para visión por computadora
import numpy as np      # NumPy: manejo de arreglos y cálculos numéricos
import os               # OS: para verificar rutas de archivos en el sistema

# 📂 Definir rutas absolutas de los archivos del modelo
prototxt = r"C:\Users\xmelx\Documents\Proyectos\DeteccionObjetos\MobileNetSSD_deploy.prototxt"  # Ruta al archivo de configuración
model = r"C:\Users\xmelx\Documents\Proyectos\DeteccionObjetos\MobileNetSSD_deploy.caffemodel"   # Ruta al archivo con pesos del modelo

# ✅ Verificación de archivos
if not os.path.exists(prototxt):   # Si no existe el archivo prototxt
    raise FileNotFoundError("No se encontró el archivo prototxt en la ruta especificada")
if not os.path.exists(model):      # Si no existe el archivo caffemodel
    raise FileNotFoundError("No se encontró el archivo caffemodel en la ruta especificada")

print("Cargando modelo...")        # Mensaje en consola
net = cv2.dnn.readNetFromCaffe(prototxt, model)  # Cargar el modelo en memoria
print("✅ Modelo cargado correctamente")         # Confirmación

# 🏷️ Lista de clases traducidas al español
CLASSES = ["fondo", "avión", "bicicleta", "pájaro", "barco",
           "botella", "autobús", "coche", "gato", "silla", "vaca", "mesa de comedor",
           "perro", "caballo", "motocicleta", "persona", "planta en maceta",
           "oveja", "sofá", "tren", "televisor"]

# 🎥 Inicializar cámara
print("Abriendo cámara...")
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)   # Abrir cámara (CAP_DSHOW evita errores en Windows)
if not cap.isOpened():                     # Si no se abre la cámara
    raise RuntimeError("Error: no se pudo abrir la cámara")

# 🔍 Bucle principal de detección
while True:
    ret, frame = cap.read()                # Leer un frame de la cámara
    if not ret:                            # Si no se pudo leer
        print("No se pudo leer frame de la cámara")
        break

    (h, w) = frame.shape[:2]               # Obtener alto y ancho del frame
    blob = cv2.dnn.blobFromImage(          # Convertir imagen a blob para el modelo
        cv2.resize(frame, (300, 300)),     # Redimensionar a 300x300
        0.007843,                          # Escalar valores de píxel
        (300, 300),                        # Tamaño de entrada
        127.5                              # Valor de normalización
    )
    net.setInput(blob)                     # Pasar blob al modelo
    detections = net.forward()             # Ejecutar detección

    # Procesar cada detección
    for i in range(detections.shape[2]):   # Iterar sobre todas las detecciones
        confianza = detections[0, 0, i, 2]   # Nivel de confianza de la detección
        if confianza > 0.5:                  # Si la confianza es mayor a 50%
            idx = int(detections[0, 0, i, 1])  # Índice de la clase detectada
            etiqueta = CLASSES[idx]            # Nombre de la clase en español
            caja = detections[0, 0, i, 3:7] * np.array([w, h, w, h])  # Coordenadas de la caja
            (startX, startY, endX, endY) = caja.astype("int")         # Convertir a enteros

            # Dibujar la caja en la imagen
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                          (0, 255, 0), 2)   # Rectángulo verde
            # Escribir etiqueta y confianza
            cv2.putText(frame, f"{etiqueta}: {confianza:.2f}",
                        (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Mostrar el frame con detecciones
    cv2.imshow("Detección de objetos", frame)

    # Salir si se presiona la tecla "q"
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 🛑 Liberar recursos al terminar
cap.release()             # Cerrar la cámara
cv2.destroyAllWindows()   # Cerrar todas las ventanas de OpenCV