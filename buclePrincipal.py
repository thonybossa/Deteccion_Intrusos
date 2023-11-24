import threading
import queue
import time
import cv2
import numpy as np
import os
import datetime
import sys

# Redirección de la salida estándar y errores estándar al archivo de log
log_file_path = "/home/ab/Deteccion_Intrusos/log_systemd_main.txt"
log_file = open(log_file_path, "a")
sys.stdout = log_file
sys.stderr = log_file


#Función encargada de almacenar las imagenes de intrusos en el buffer
def guardarBuffer(imagen):
    # Obtener la fecha y hora actual
    ahora = datetime.datetime.now()
    formato_fecha_hora = ahora.strftime("%Y%m%d_%H%M%S")

    directorio = "./buffer/"
    ruta_imagen = directorio+f"imagen_{formato_fecha_hora}.jpg"

    # Guardar la imagen en formato jpg
    cv2.imwrite(ruta_imagen, imagen)

    print(f"Imagen guardada en: {ruta_imagen}")

#Función responsable de la creación el buffer si este no existe
def verBuffer():
    ruta_carpeta="./buffer"
    # Verificar si la carpeta existe
    if not os.path.exists(ruta_carpeta):
        try:
            # Crear la carpeta si no existe
            os.makedirs(ruta_carpeta)
            print(f'Carpeta creada en: {ruta_carpeta}')
        except OSError as e:
            print(f'Error al crear buffer: {e}')
    else:
        print(f'Buffer ya existe en: {ruta_carpeta}')


#Función para detectar rostros
def detectarRostro(imagen):
    
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


#Función de detección de movimiento
def detectarMovimiento(imagen1, imagen2, umbral=30):
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

# Función que representa al hilo que captura imágenes
def capturador(q):
    while (True):
        # Inicializar la cámara
        camera = cv2.VideoCapture(0)  
        if not camera.isOpened():
            print("Soy el capturador, no se pudo abrir la cámara.")
        else:
            # Capturar una imagen
            return_value, image = camera.read()
            if return_value:
                q.put(image)
            else:
                print("Soy el capturador, no se pudo capturar la imagen.")

        # Liberar la cámara
        camera.release()
        cv2.destroyAllWindows()
        time.sleep(1)

# Función que representa al hilo que detecta movimiento
def detectorMov(q1,q2):
    previa = q1.get()
    q1.task_done()    
    while True:
        actual = q1.get()
        if actual is None:
            break
        flag = detectarMovimiento(previa, actual)
        
        if flag:
            print("Soy el detecMov ¡Se detectó movimiento!")
            q2.put(actual)
        else:
            print(" Soy el detecMov, No hubo movimiento.")
        
        previa=actual 
        q1.task_done()

# Función que representa al hilo que detecta rostros de personas
def detectorFace(q):
    while True:
        img = q.get()
        if img is None:
            break
        flag = detectarRostro(img)
        
        if flag:
            print("Soy el detecFace ¡Se detectó un intruso!")
            #Almacenar en buffer
            guardarBuffer(img)
        else:
            print(" Soy el detecFace, No hay intrusos.")
        
        q.task_done()



# Se verifica o se crea el buffer de imágenes
verBuffer()

# Colas compartidas entre los hilos
queue1 = queue.Queue()
queue2 = queue.Queue()

# Crear los hilos
hiloCapturador = threading.Thread(target=capturador, args=(queue1,))
hiloDetecMov = threading.Thread(target=detectorMov, args=(queue1,queue2,))
hiloDetecFace = threading.Thread(target=detectorFace, args=(queue2,))


# Iniciar los hilos
hiloCapturador.start()
hiloDetecMov.start()
hiloDetecFace.start()

# Esperar a que el hilo productor termine su trabajo
hiloCapturador.join()

# Indicar a los hilos que no hay más datos
queue1.put(None)
queue2.put(None)

# Esperar a que el hilo consumidor termine su trabajo
hiloDetecMov.join()
hiloDetecFace.join()

print("Proceso terminado")

