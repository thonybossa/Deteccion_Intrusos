import cv2
import numpy as np

def detectar_movimiento(imagen1, imagen2, umbral=30):
    # Convierte las imágenes a escala de grises
    gris1 = cv2.cvtColor(imagen1, cv2.COLOR_BGR2GRAY)
    gris2 = cv2.cvtColor(imagen2, cv2.COLOR_BGR2GRAY)

    # Calcula la diferencia absoluta entre las dos imágenes
    diferencia = cv2.absdiff(gris1, gris2)

    # Aplica un umbral a la diferencia para obtener una imagen binaria
    _, umbralizado = cv2.threshold(diferencia, umbral, 255, cv2.THRESH_BINARY)

    # Encuentra los contornos en la imagen umbralizada
    contornos, _ = cv2.findContours(umbralizado, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Si hay contornos, hay movimiento
    if len(contornos) > 0:
        return True
    else:
        return False

# Ejemplo de uso:
# Lee dos imágenes
imagen1 = cv2.imread('imagen1.jpg')
imagen2 = cv2.imread('imagen1.jpg')

# Llama a la función para detectar movimiento
hubo_movimiento = detectar_movimiento(imagen1, imagen2)

# Imprime el resultado
if hubo_movimiento:
    print("¡Se detectó movimiento!")
else:
    print("No hubo movimiento.")

