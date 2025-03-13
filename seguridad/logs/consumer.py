import pika
import os
import time

# Configuración de RabbitMQ desde variables de entorno
rabbitmq_host = os.getenv("RABBITMQ_HOST", "rabbitmq")
rabbitmq_user = os.getenv("RABBITMQ_USER", "user")
rabbitmq_password = os.getenv("RABBITMQ_PASSWORD", "password")
queue_name = "logs"
log_file_path = "./logs.txt"

# Asegurar que logs.txt existe antes de escribir en él
open(log_file_path, "a").close()

# Intentar conectar con RabbitMQ con reintentos
while True:
    try:
        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
        parameters = pika.ConnectionParameters(host=rabbitmq_host, credentials=credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Asegurar que la cola existe
        channel.queue_declare(queue=queue_name, durable=True)

        print("Conectado a RabbitMQ y escuchando la cola de logs...")

        # Función para procesar los mensajes de la cola
        def callback(ch, method, properties, body):
            mensaje = body.decode("utf-8")
            print(f"Recibido: {mensaje}")

            # Guardar el log en logs.txt
            with open(log_file_path, "a") as log_file:
                log_file.write(mensaje + "\n")

            # Confirmar que el mensaje fue procesado
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # Configurar el consumidor
        channel.basic_consume(queue=queue_name, on_message_callback=callback)

        # Iniciar la escucha de mensajes
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError:
        print("RabbitMQ no está listo. Reintentando en 5 segundos...")
        time.sleep(5)
    except Exception as e:
        print(f"Error inesperado: {e}")
        break  # Si hay otro error, salir del bucle
