import os

from flask import Flask, request, jsonify
import pika
import json

from cliente_autorizador import ClienteAutorizador

app = Flask(__name__)

# Configurar conexión a RabbitMQ
rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
queue_name = os.getenv("NOMBRE_COLA")


def send_log(username, action, data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    log_entry = {"username": username, "action": action, "data": data}

    channel.basic_publish(
        exchange="", routing_key=queue_name, body=json.dumps(log_entry)
    )
    connection.close()


# Inventario (simulado en memoria)
inventario = []


def verificar_autorizacion(token: str) -> bool:
    cliente_autorizador = ClienteAutorizador(token=token)

    return cliente_autorizador.autorizar()


@app.route("/productos", methods=["GET"])
def obtener_productos():
    token = request.headers.get("Authorization").replace("Bearer ", "")
    if not verificar_autorizacion(token):
        return jsonify({"error": "No Autorizado"}), 401
    return jsonify(inventario)


@app.route("/productos", methods=["POST"])
def agregar_producto():
    token = request.headers.get("Authorization").replace("Bearer ", "")
    if not verificar_autorizacion(token):
        return jsonify({"error": "No Autorizado"}), 401
    data = request.json
    username = request.headers.get("Username", "unknown_user")
    if "nombre" not in data:
        return jsonify({"error": "El producto debe tener un nombre"}), 400

    inventario.append(data["nombre"])
    send_log(username, "POST", data["nombre"])
    return jsonify({"mensaje": "Producto agregado"}), 201


@app.route("/productos/<nombre>", methods=["DELETE"])
def eliminar_producto(nombre):
    token = request.headers.get("Authorization").replace("Bearer ", "")
    if not verificar_autorizacion(token):
        return jsonify({"error": "No Autorizado"}), 401
    username = request.headers.get("Username", "unknown_user")
    if nombre in inventario:
        inventario.remove(nombre)
        send_log(username, "DELETE", nombre)
        return jsonify({"mensaje": "Producto eliminado"}), 200
    return jsonify({"error": "Producto no encontrado"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
