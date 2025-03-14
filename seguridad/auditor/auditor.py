import asyncio
import logging
import os
from enum import StrEnum, auto

import requests

from disponibilidad.servicios.rabbitMQ.subscriptor import Subscriptor

QUEUE_NAME = os.getenv("QUEUE_NAME")
AUTORIZADOR_URL = os.getenv("AUTORIZADOR_URL")
USUARIO_OAUTH = "auditor"

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s|[%(levelname)s]|%(asctime)s|%(message)s",
    handlers=[
        logging.FileHandler(f"logs/auditor.log", mode="w"),
        logging.StreamHandler(),
    ],
)
logging.getLogger("pika").setLevel(logging.WARNING)


class LogLevelType(StrEnum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


log_level_map = {
    "DEBUG": logging.debug,
    "INFO": logging.info,
    "WARNING": logging.warning,
    "ERROR": logging.error,
    "CRITICAL": logging.critical,
}


def obtener_token():
    response = requests.post(f"{AUTORIZADOR_URL}/token/{USUARIO_OAUTH}", verify=False)
    return response.json()["token"]


subscriptor = Subscriptor(token=obtener_token(), username=USUARIO_OAUTH)


def callback(ch, method, properties, body):
    log_level = (
        properties.headers.get("log_level", "INFO")
        if properties and properties.headers
        else "INFO"
    )
    log_func = log_level_map.get(log_level, logging.info)
    log_func(body.decode("utf-8"))


async def main():
    await subscriptor.suscribirse(
        nombre_cola=QUEUE_NAME, routing_key=QUEUE_NAME, callback=callback
    )
    while True:
        pass


asyncio.run(main())
