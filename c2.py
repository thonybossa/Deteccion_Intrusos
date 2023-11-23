import cv2

# Inicializar la cámara de la Raspberry Pi
camera = cv2.VideoCapture(0)  # 0 es el índice de la cámara predeterminada (puede variar)

if not camera.isOpened():
    print("No se pudo abrir la cámara.")
else:
    # Capturar una imagen
    return_value, image = camera.read()
    if return_value:
        # Guardar la imagen capturada en un archivo
        cv2.imwrite('imagen2.jpg', image)
        print("Imagen capturada y guardada como imagen_capturada.jpg")
    else:
        print("No se pudo capturar la imagen.")

    # Liberar la cámara
    camera.release()

# Cerrar la ventana de la cámara
cv2.destroyAllWindows()

