from datetime import datetime, timedelta
import jwt
import json
import logging
import os
from disponibilidad.servicios.rabbitMQ.subscriptor import Subscriptor

logger = logging.getLogger(__name__)

class Detector:

    @property
    def lista_blanca(self):
        return "This is a readonly property"
    
    def __init__(self):
        self._lista_blanca = self.obtener_lista_blanca()
        self.cofiguracion_detector()
        
    def obtener_lista_blanca(self):
        return json.loads(json.dumps(os.getenv('ORIGENES_AUTORIZADOS', '[]')))
        
    def cofiguracion_detector(self):
        self.subscriptor = Subscriptor(token=self.generar_jwt())
        self.inventory_routing_key = 'inventory-audit'
        self.nombre_cola_inventory = 'inventory-audit'
        
    def evento_mensaje_nuevo(self, ch, method, properties, body):
        body_str = body.decode("utf-8")
        self.validar_mensaje(body_str)
        self.validar_intrusion(body_str)
                
    async def start(self):
        await self.subscriptor.suscribirse(
            nombre_cola=self.nombre_cola_inventory, 
            routing_key=self.inventory_routing_key, 
            callback=self.evento_mensaje_nuevo
        )
        while True:
            pass    
        
    def validar_mensaje(self, mensaje):
        deserialize = json.loads(mensaje)
        resumen = hash(json.dumps(deserialize.get('message')))
        if(resumen != deserialize.get('check_sum')):
            logger.warning(f"Mensaje alterado|{mensaje}")
            
    def validar_intrusion(self, mensaje):
        deserialize = json.loads(mensaje)
        host_ip = deserialize.get('message').get('host_ip')
        if(not self._lista_blanca.__contains__(host_ip)):
            logger.warning(f"Mensaje con origen no válido desde la IP {host_ip}|{mensaje}")
            
    def generar_jwt(self):
        payload = {
            "sub": "detector",  # Username
            "aud": "inventario-test",   # Must match RabbitMQ's configured audience
            "iat": datetime.now(),  # Issued at
            "exp": datetime.now() + timedelta(minutes=7200)  # Expiration time
        }
        return jwt.encode(payload, "inventario-test-key", algorithm="HS256")