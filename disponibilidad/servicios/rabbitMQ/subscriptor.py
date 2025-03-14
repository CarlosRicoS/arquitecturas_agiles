import os
import threading
import pika
import logging
from pika.credentials import PlainCredentials

logger = logging.getLogger(__name__)
rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")


class Subscriptor:

    def __init__(self, token=None, username: str = None):
        self.token = token
        self.username = username
        self.host = rabbitmq_host
        self.nombre_exchange = "monitor"
        self.tipo_exchange = "direct"
        self.configuracion_mensajeria()

    async def suscribirse(self, nombre_cola, routing_key, callback):
        print("Inicio suscripción")
        self.channel.queue_declare(queue=nombre_cola)
        self.channel.queue_bind(
            exchange=self.nombre_exchange, queue=nombre_cola, routing_key=routing_key
        )
        self.channel.basic_consume(
            queue=nombre_cola, on_message_callback=callback, auto_ack=True
        )

        thread = threading.Thread(target=self.channel.start_consuming, daemon=True)
        thread.start()
        logger.info("Suscripción configurada")

    def configuracion_mensajeria(self):
        jwt_token = PlainCredentials(username=self.username, password=self.token)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                credentials=jwt_token,
            )
        )
        self.channel = self.connection.channel()

        self.channel.exchange_declare(
            exchange=self.nombre_exchange, exchange_type=self.tipo_exchange
        )
