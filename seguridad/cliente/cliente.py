import os
import random
from functools import partial
from time import sleep

import requests

INVENTARIO_URL = os.getenv("INVENTARIO_URL")
ACCIONES = [
    ("POST", "/productos"),
    ("GET", "/productos"),
    ("DELETE", "/productos/<nombre>"),
]
USUARIO_OAUTH = os.getenv("USUARIO_OAUTH")
AUTORIZADOR_URL = os.getenv("AUTORIZADOR_URL")
CANTIDAD_SOLICITUDES = os.getenv("CANTIDAD_SOLICITUDES")
NOMBRE_PRODUCTOS = [
    "producto_1",
    "producto_2",
    "producto_3",
    "producto_4",
    "producto_5",
]

solicitud_funciones = {
    "POST": partial(requests.post),
    "GET": partial(requests.get),
    "DELETE": partial(requests.delete),
}


def generar_token():
    response = requests.post(f"{AUTORIZADOR_URL}/token/{USUARIO_OAUTH}", verify=False)
    return response.json()["token"]


def ejecutar_solicitud(accion: tuple[str, str], data: dict[str, str] = None) -> None:
    funcion = partial(
        solicitud_funciones[accion[0]], url=f"{INVENTARIO_URL}{accion[1]}"
    )
    headers = {"Authorization": f"Bearer {generar_token()}"}
    if data:
        funcion(json=data, headers=headers)
    else:
        funcion(headers=headers)


def main() -> None:
    for _ in range(int(CANTIDAD_SOLICITUDES)):
        data = None
        accion = random.choice(ACCIONES)
        if accion[0] == "POST" or accion[0] == "DELETE":
            data = {"nombre": random.choice(NOMBRE_PRODUCTOS)}
        ejecutar_solicitud(accion, data)
        sleep(1)


if __name__ == "__main__":
    main()
