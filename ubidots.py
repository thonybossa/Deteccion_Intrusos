import requests
import random
import time

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

# Main loop for continuous data sending
while True:
    sendNube()
    time.sleep(10) 
    

