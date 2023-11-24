import socket
from imagekitio import ImageKit
from base64 import b64encode
import os
import requests
import datetime
import sys

# Clase para manejar la salida del log
class Logger(object):
    def __init__(self, filename, max_lines=50):
        self.terminal = sys.stdout
        self.log = open(filename, "a")
        self.filename = filename
        self.max_lines = max_lines
        self.line_count = 0

    def write(self, message):
        self.terminal.write(message)
        self.log.write(f"{datetime.datetime.now().isoformat()} - {message}")
        self.line_count += 1
        if self.line_count > self.max_lines:
            self.trim_log()

    def trim_log(self):
        with open(self.filename, "r") as file:
            lines = file.readlines()
        with open(self.filename, "w") as file:
            file.writelines(lines[-self.max_lines:])
        self.line_count = self.max_lines

    def flush(self):
        pass

# Redirección de la salida estándar y errores estándar al archivo de log
sys.stdout = Logger("/home/ab/Deteccion_Intrusos/log_systemd_cloud.txt")
sys.stderr = sys.stdout

# Redirección de la salida estándar y errores estándar al archivo de log
sys.stdout = Logger("/home/ab/Deteccion_Intrusos/log_systemd_cloud.txt")
sys.stderr = sys.stdout

# Redirección de la salida estándar y errores estándar al archivo de log
#log_file_path = "/home/ab/Deteccion_Intrusos/log_systemd_cloud.txt"
#log_file = open(log_file_path, "a")
#sys.stdout = log_file
#sys.stderr = log_file


#Revisa si hay internet
def checkNet():
    try:
        # Si conecta con google es que hay internet
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        print("Conectado")
        return True
    except OSError:
        print("No hay nternet")
        return False

#Sube la imagen del intruso a la nube
def upload(img,image_path):

    nombre=image_path[9:]

    # Configura tus credenciales de ImageKit
    tk = ImageKit(
        private_key="private_aCNBgmVlr21paDKQdv+Td93l70I=",
        public_key="public_mgratcvyVArSW2M9XugG3+LmE8w=",
        url_endpoint="https://ik.imagekit.io/DeteccionIntrusos"
    )

    # Sube imagen
    res = tk.upload_file(img,file_name=nombre)

    # codigo
    code = res.response_metadata.http_status_code

    return code

# Ubidots API settings
UBIDOTS_TOKEN = "BBUS-8PLTjPFY4mvca2xCvmMyWyPXE80G5z"
VARIABLE_ID = "flag"
API_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/default/{VARIABLE_ID}/values"

# Función encargada de comunicar el evento a Ubidots
def sendNube():
    payload = {"value": 1}
    headers = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}
    response = requests.post(API_URL, json=payload, headers=headers)
    
    if response.status_code == 201:
        print(f" Se ha detectado un intruso, aviso a las autoridades competentes")
    else:
        print(f"Comunicación fallida, código: {response.status_code}")

#Path del buffer
path="/home/ab/Deteccion_Intrusos/buffer"

while(True):
    if (checkNet()):
        for file in os.listdir(path):
            if file.endswith(('.jpg')): 
                img_path = os.path.join(path, file)
                with open (img_path,"rb") as f:
                    img = b64encode(f.read())
                    if img is not None:
                        print("Subiendo imagen")
                        code=upload(img,img_path)
                        sendNube()
                        if(code==200):
                            print("imagen subida")
                            os.remove(img_path)
                    


