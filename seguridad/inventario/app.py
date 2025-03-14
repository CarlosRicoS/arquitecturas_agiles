import logging
import os
import uuid
from datetime import datetime

import requests
from flask import Flask, request, jsonify

from cliente_autorizador import ClienteAutorizador
from disponibilidad.servicios.rabbitMQ.publicador import Publicador
from seguridad.common.inventory_audit_message import Inventory_Audit_Message


QUEUE_NAME = os.getenv("NOMBRE_COLA")
AUTORIZADOR_URL = os.getenv("AUTORIZADOR_URL")
USUARIO_OAUTH = "publisher"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s|[%(levelname)s]|%(asctime)s|%(message)s",
    handlers=[
        logging.FileHandler(f"logs/inventario.log", mode="w"),
        logging.StreamHandler(),
    ],
)

logging.getLogger("pika").setLevel(logging.CRITICAL)
logging.getLogger("werkzeug").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)

app = Flask(__name__)


def generar_oauth_token():
    response = requests.post(f"{AUTORIZADOR_URL}/token/{USUARIO_OAUTH}", verify=False)
    token = response.json()["token"]
    return token


publicador = None


def get_publicador():
    global publicador
    if publicador is None:
        publicador = Publicador(token=generar_oauth_token(), username=USUARIO_OAUTH)
    return publicador


def definir_mensaje(detalle, ip):
    inventory_audit_message = Inventory_Audit_Message(
        detail=detalle,
        event_type="CAMBIO-INVENTARIO",
        uuid=str(uuid.uuid4()),
        timestamp=datetime.now().isoformat(),
        host_ip=ip,
    )

    return inventory_audit_message.get_message()


def publicar_log(detalle, ip):
    get_publicador()
    mensaje = definir_mensaje(detalle, ip)
    publicador.escribir_mensajes(
        routing_key=QUEUE_NAME, mensaje=mensaje, log_level=logging.INFO
    )
    logging.debug(f"[Inventario] Sent {mensaje}")


# Inventario (simulado en memoria)
inventario = []


def verificar_autorizacion(method: str, path: str, token: str) -> str | None:
    cliente_autorizador = ClienteAutorizador(token=token)

    return cliente_autorizador.autorizar(method, path)


@app.route("/productos", methods=["GET"])
def obtener_productos():
    token = request.headers.get("Authorization").replace("Bearer ", "")
    usuario_autorizado = verificar_autorizacion("GET", "/productos", token)
    if not usuario_autorizado:
        return jsonify({"error": "No Autorizado"}), 401
    detalle_mensaje = {
        "usuario": usuario_autorizado,
        "accion": "GET",
        "data": inventario,
    }
    publicar_log(detalle_mensaje, request.remote_addr)
    return jsonify(inventario)


@app.route("/productos", methods=["POST"])
def agregar_producto():
    token = request.headers.get("Authorization").replace("Bearer ", "")
    usuario_autorizado = verificar_autorizacion("POST", "/productos", token)
    if not usuario_autorizado:
        return jsonify({"error": "No Autorizado"}), 401
    data = request.json
    if "nombre" not in data:
        return jsonify({"error": "El producto debe tener un nombre"}), 400

    inventario.append(data["nombre"])
    detalle_mensaje = {
        "usuario": usuario_autorizado,
        "accion": "POST",
        "data": data["nombre"],
    }
    publicar_log(detalle_mensaje, request.remote_addr)
    return jsonify({"mensaje": "Producto agregado"}), 201


@app.route("/productos/<nombre>", methods=["DELETE"])
def eliminar_producto(nombre):
    token = request.headers.get("Authorization").replace("Bearer ", "")
    usuario_autorizado = verificar_autorizacion("DELETE", "/productos/<nombre>", token)
    if not usuario_autorizado:
        return jsonify({"error": "No Autorizado"}), 401
    if nombre in inventario:
        inventario.remove(nombre)
        detalle_mensaje = {
            "usuario": usuario_autorizado,
            "accion": "DELETE",
            "data": nombre,
        }
        publicar_log(detalle_mensaje, request.remote_addr)
        return jsonify({"mensaje": "Producto eliminado"}), 200
    return jsonify({"error": "Producto no encontrado"}), 404


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
