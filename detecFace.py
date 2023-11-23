import cv2

def detectar_rostro_en_imagen(imagen_path):
    # Cargar la imagen
    imagen = cv2.imread(imagen_path)
    
    # Convertir la imagen a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    
    # Cargar el clasificador Haarcascade para la detección de rostros
    clasificador_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detectar rostros en la imagen
    rostros = clasificador_rostros.detectMultiScale(gris, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    
    if len(rostros) > 0:
        return True
    else:
        return False


imagen_contiene_rostro = detectar_rostro_en_imagen('rostro1.jpg')

if imagen_contiene_rostro:
    print("La imagen contiene un rostro.")
else:
    print("La imagen no contiene un rostro.")

