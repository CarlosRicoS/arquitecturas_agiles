import os
import logging
import pika
from pika.credentials import PlainCredentials

logger = logging.getLogger(__name__)
rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")


class Publicador:

    def __init__(self, token: str = None, username: str = None):
        self.token = token
        self.username = username
        self.host = rabbitmq_host
        self.nombre_exchange = "monitor"
        self.tipo_exchange = "direct"
        self.configuracion_mensajeria()

    def escribir_mensajes(self, routing_key, mensaje, log_level):
        properties = pika.BasicProperties(headers={"log_level": log_level})
        self.channel.basic_publish(
            exchange=self.nombre_exchange,
            routing_key=routing_key,
            body=mensaje,
            properties=properties,
        )

    def configuracion_mensajeria(self):
        jwt_token = PlainCredentials(username=self.username, password=self.token)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host, credentials=jwt_token)
        )
        self.channel = self.connection.channel()

        self.channel.exchange_declare(
            exchange=self.nombre_exchange, exchange_type=self.tipo_exchange
        )
