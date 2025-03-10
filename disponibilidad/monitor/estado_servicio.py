from datetime import datetime

class EstadoServicio:
    @property
    def marca_error(self):
        return self._marca_error
    
    @marca_error.setter
    def marca_error(self, value):
        self._marca_error = value
    
    @property
    def ultimo_reporte(self):
        return self._ultimo_reporte
    
    @ultimo_reporte.setter
    def ultimo_reporte(self, value):
        if not value:
            raise ValueError("Valor no válido")
        self._ultimo_reporte = value
        
    @property
    def nombre_instancia(self):
        return self._nombre_instancia
    
    def __init__(self, nombre_instancia):
        self._marca_error = None
        self._nombre_instancia = nombre_instancia
        self._ultimo_reporte = datetime.now() 
 