import threading
import pika 
import asyncio

class Subscriptor:
      
    def __init__(self):
        self.host = 'rabbitmq' # localhost
        self.nombre_exchange = 'monitor'
        self.tipo_exchange = 'direct'
        self.configuracion_mensajeria()   
        print("Mensajería configurada")
        
    async def suscribirse(self, nombre_cola, routing_key, callback):
        print("Iniico suscripción")      
        self.channel.queue_declare(queue=nombre_cola)
        self.channel.queue_bind(
            exchange=self.nombre_exchange, 
            queue=nombre_cola, 
            routing_key=routing_key
        )
        self.channel.basic_consume(queue=nombre_cola, on_message_callback=callback, auto_ack=True)
        
        thread = threading.Thread(target=self.channel.start_consuming, daemon=True)
        thread.start()
        print("suscripción configurada")      

    def configuracion_mensajeria(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.nombre_exchange, exchange_type=self.tipo_exchange)
        