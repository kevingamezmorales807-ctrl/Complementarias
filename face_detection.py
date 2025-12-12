import cv2
import os

carpeta_origen = "data/sofia_fotos"
carpeta_salida = "data/sofia"

os.makedirs(carpeta_salida, exist_ok=True)

detector_rostros = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

contador = 0

for archivo in os.listdir(carpeta_origen):
    if not (archivo.lower().endswith(".jpg") or archivo.lower().endswith(".png") or archivo.lower().endswith(".jpeg")):
        continue

    ruta = os.path.join(carpeta_origen, archivo)
    img = cv2.imread(ruta)

    if img is None:
        print("No se pudo leer:", ruta)
        continue

    gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rostros = detector_rostros.detectMultiScale(gris, 1.3, 5)

    if len(rostros) == 0:
        print("No se detectó rostro en:", archivo)
        continue

    x, y, w, h = rostros[0]
    rostro = gris[y:y + h, x:x + w]
    rostro = cv2.resize(rostro, (200, 200))

    nombre_salida = os.path.join(carpeta_salida, f"sofia_{contador}.jpg")
    cv2.imwrite(nombre_salida, rostro)
    contador += 1
    print("Rostro guardado en:", nombre_salida)

print(f"Listo. Se guardaron {contador} rostros recortados en {carpeta_salida}.")