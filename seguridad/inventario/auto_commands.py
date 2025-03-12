import requests
import time

API_URL = "http://inventario_service:5000/productos"

def ejecutar_comandos_automaticamente():
    productos = ["Laptop", "Teclado", "Mouse", "Monitor", "Impresora"]
    
    for producto in productos:
        response = requests.post(API_URL, json={"nombre": producto}, headers={"Username": "auto_script"})
        print(f"Agregado {producto}: {response.status_code}")
        time.sleep(2)  # Esperar 2 segundos entre comandos
    
    response = requests.get(API_URL + "/productos")
    print(f"Productos: {response.status_code}")

    for producto in productos:
        response = requests.delete(API_URL + "/" + producto, headers={"Username": "auto_script"})
        print(f"Eliminado {producto}: {response.status_code}")

if __name__ == "__main__":
    time.sleep(10)  # Esperar a que el servicio de inventario esté listo
    ejecutar_comandos_automaticamente()
