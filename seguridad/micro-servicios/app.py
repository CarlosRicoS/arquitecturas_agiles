from flask import Flask, request, jsonify
import json
import pika
import time

app = Flask(__name__)

def conectar_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
            print("✅ Conectado a RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("⏳ Esperando RabbitMQ...")
            time.sleep(5)  # Reintentar cada 5 segundos

username = "admin"
# Cargar inventario
with open("inventory.json", "r") as f:
    inventario = json.load(f)

connection = conectar_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue="logs")



# Endpoints API
@app.route("/inventario", methods=["GET"])
def obtener_inventario():
    mensaje = f"Usuario: {username} - Acción: consultó los productos"
    channel.basic_publish(exchange="", routing_key="logs", body=mensaje)

    return jsonify({"mensaje": "Producto consultado"}), 201

@app.route('/inventario', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    
    try:
        with open("inventario.json", "r") as file:
            inventario = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        inventario = []  # Si el archivo está vacío o no existe, inicializa como lista

    if not isinstance(inventario, list):
        return jsonify({"error": "El archivo JSON no tiene formato de lista"}), 500

    inventario.append(data)

    with open("inventario.json", "w") as file:
        json.dump(inventario, file, indent=4)
    
    # 🔍 Agrega este print para verificar que se escribió correctamente
    print("📁 Inventario actualizado:", inventario)
    mensaje = f"Usuario: {username} - Acción: Agregó el producto '{data}'"
    channel.basic_publish(exchange="", routing_key="logs", body=mensaje)
    return jsonify({"mensaje": "Producto agregado"}), 201

@app.route("/inventario/<string:nombre>", methods=["DELETE"])
def eliminar_producto(nombre):
    try:
        with open("inventario.json", "r") as file:
            inventario = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        inventario = []  # Si el archivo está vacío o no existe, inicializa como lista

    # Filtrar productos y verificar si se encontró
    nuevo_inventario = [p for p in inventario if p["nombre"] != nombre]

    if len(nuevo_inventario) == len(inventario):
        mensaje = f"Usuario: {username} - Acción: Producto '{nombre}' NO encontrado para eliminar"
        channel.basic_publish(exchange="", routing_key="logs", body=mensaje)
        return jsonify({"mensaje": "Producto NO encontrado"}), 404

    # Guardar cambios en el archivo
    with open("inventario.json", "w") as file:
        json.dump(nuevo_inventario, file, indent=4)

    mensaje = f"Usuario: {username} - Acción: Eliminó producto '{nombre}'"
    channel.basic_publish(exchange="", routing_key="logs", body=mensaje)

    return jsonify({"mensaje": f"Producto '{nombre}' eliminado"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)