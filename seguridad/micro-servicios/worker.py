import requests
import time

API_URL = "http://microservicio:5000/inventario"

while True:
    response = requests.get(API_URL)
    print("Estado del inventario:", response.json())

    time.sleep(5)  # Ejecuta cada 10 segundos