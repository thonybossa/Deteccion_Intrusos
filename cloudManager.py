import socket
from imagekitio import ImageKit
from base64 import b64encode
import os
import requests

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
        private_key="",
        public_key="",
        url_endpoint=""
    )

    # Sube imagen
    res = tk.upload_file(img,file_name=nombre)

    # codigo
    code = res.response_metadata.http_status_code

    return code

# Ubidots API settings
UBIDOTS_TOKEN = "BBUS-V4bpLQ0MZYdUGWwFRBEsmyfpb6UWf1"
VARIABLE_ID = "text"
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
path="/home/gomezan/Documents/deteccionIntrusos/buffer"

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
                    


