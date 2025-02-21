import threading
import uuid
import os
from datetime import datetime, timedelta
from monitor.estado_servicio import EstadoServicio
from servicios.rabbitMQ.publicador import Publicador
from servicios.rabbitMQ.subscriptor import Subscriptor

import logging

logger = logging.getLogger(__name__)

class Monitor:
    def __init__(self):
        self.cofiguracion_monitor()
    
    def cofiguracion_monitor(self):
        # Configura estado inicial de microservicios
        self.instancias = { 
            "principal": EstadoServicio(nombre_instancia='principal'),
            "respaldo": EstadoServicio(nombre_instancia='respaldo')
        }
        # Configura mensajeria 
        self.subscriptor = Subscriptor()
        self.publicador = Publicador()
        self.error_routing_key = 'error'
        self.healthcheck_routing_key = 'healthcheck'
        self.nombre_cola_healthcheck = 'healthcheck'
        self.frecuencia_monitoreo = os.getenv('MONITOR_FREQ_S', '2')
        self.max_retrazo_healtcheck = os.getenv('MAX_SERVICE_DELAY_MS', '2100')
        
    # callback para cálculo de estado de servicios
    def monitorear_estado(self):
        [self.validar_servicios(instancia) for instancia in self.instancias.keys()]
        self.inicio_timer()

    def inicio_timer(self):
        timer = threading.Timer(
            float(self.frecuencia_monitoreo), 
            self.monitorear_estado
        )
        timer.start()        
        
    def validar_servicios(self, nombre_instancia):
        if self.es_servicio_indispuesto(self.instancias[nombre_instancia]):
            self.publicar_error_servicio(nombre_instancia)
            
    def es_servicio_indispuesto(self, instancia):
        difference = datetime.now() - instancia.ultimo_reporte
        return difference > timedelta(milliseconds=int(self.max_retrazo_healtcheck))
    
    def evento_mensaje_nuevo(self, ch, method, properties, body):
        body_str = body.decode("utf-8")
        self.instancias[body_str].ultimo_reporte = datetime.now()
        self.instancias[body_str].marca_error = None
    
    def publicar_error_servicio(self, nombre_instancia):
        marca_error = self.obtener_marca_error(nombre_instancia)
        mensaje_error = f"{marca_error} | {nombre_instancia}"
        logging.error(mensaje_error)
        self.publicador.escribir_mensajes(
            routing_key=self.error_routing_key, 
            mensaje=mensaje_error,
            log_level="ERROR"
        )
    
    def obtener_marca_error(self, nombre_instancia):
        marca_error = self.instancias[nombre_instancia].marca_error
        if marca_error is None:
            self.instancias[nombre_instancia].marca_error = uuid.uuid4().hex
            marca_error = self.instancias[nombre_instancia].marca_error
        return marca_error
        
    async def start(self):
        await self.subscriptor.suscribirse(
            nombre_cola=self.nombre_cola_healthcheck, 
            routing_key=self.healthcheck_routing_key, 
            callback=self.evento_mensaje_nuevo
        )
        self.inicio_timer()
        logging.info('|Inicio monitoreo')
        while True:
            pass    