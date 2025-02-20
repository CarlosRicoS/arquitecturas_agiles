import pika 

class Publicador:
      
    def __init__(self):
        self.host = 'rabbitmq' # localhost
        self.nombre_exchange = 'monitor'
        self.tipo_exchange = 'direct'
        self.configuracion_mensajeria()   
        print("Mensajería configurada")

    def escribir_mensajes(self, routing_key, mensaje):
        self.channel.basic_publish(exchange=self.nombre_exchange, routing_key=routing_key, body=mensaje)

    def configuracion_mensajeria(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange=self.nombre_exchange, exchange_type=self.tipo_exchange)
        