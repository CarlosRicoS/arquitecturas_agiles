import pika
import logging
import time

def conectar_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
            print("✅ Conectado a RabbitMQ")
            return connection
        except pika.exceptions.AMQPConnectionError:
            print("⏳ Esperando RabbitMQ...")
            time.sleep(5)  # Reintentar cada 5 segundos


# Configuración de logs
logging.basicConfig(filename="/logs/eventos.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Conectar a RabbitMQ
connection = conectar_rabbitmq()
channel = connection.channel()
channel.queue_declare(queue="logs")

# Callback para recibir mensajes
def callback(ch, method, properties, body):
    mensaje = body.decode()
    logging.info(mensaje)
    print("Log registrado:", mensaje)

channel.basic_consume(queue="logs", on_message_callback=callback, auto_ack=True)

print("Esperando logs...")
channel.start_consuming()