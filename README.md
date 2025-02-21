# Experimento Arquitecturas Ágiles


| Titulo del experimento                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Propósito del experimento              | Intentar detectar fallas a través del reporte del heartbeat mediante comunicación<br/> asincrónica y reportar el fallo de alguna instancia de un micro-servicio.                                                                                                                                                                                                                                                                                                                                              |
| Resultados esperados                   | Lograr generar el reporte del fallo en menos de 2 segundos. <br/> Detectar el 100% de fallas generadas en el sistema                                                                                                                                                                                                                                                                                                                                                                                          |
| Recursos requeridos                    | Docker/Kubernetes - Minikube, Message broker - RabbitMQ                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| Elementos de arquitectura involucrados | Identificador del ASR: <br/> Disponibilidad: Se deben detectar el 100% de las fallas de los micro-servicios.<br/><br/> Elementos de arquitectura:<br/> Componente Monitor<br/> Componente Broker de mensajes<br/> Componente Micro-servicio de consultas<br/><br/> Vista Funcional – Modelo Componente Conector<br/><br/> Puntos de sensibilidad:<br/> Utilizar un heartbeat con comunicación asíncrona para el monitoreo de los servicios<br/> Utilizar comunicación asíncrona para el reporte de las fallas |
| Esfuerzo estimado                      | 32 horas totales (8 horas hombre) x 4 personas                                                                                                                                                                                                                                                                                                                                                                                                                                                                | 

# Instrucciones para configurar el experimento
Para correr el experimento se debe clonar el repositorio desde la rama `main`, adicionalmente se requiere tener **docker** y **docker compose** instalado.

1. Se debe ejecutar el siguiente comando para levantar los micro-servicios y ejecutar el experimento: 
    ```
    docker compose up
    ```
2. Esperar a que se ejecuten las pruebas del experimento.
3. Verificar que el experimento corra satisfactoriamente revisando los logs en el directorio `logs` (se crean varios archivos). Validar el archivo `run_experimento.log` un ejemplo de este cuando el experimento corre satisfactoriamente: 
   ```
    2025-02-21 01:55:45 - Inicio Experimento
    2025-02-21 01:55:45 - Call 1: "en mantenimiento"
    2025-02-21 01:55:46 - Call 2: "en mantenimiento"
    2025-02-21 01:55:50 - Call 3: "indispuesto"
    2025-02-21 01:55:54 - Call 4: "indispuesto"
    2025-02-21 01:55:55 - Call 5: "en mantenimiento"
    2025-02-21 01:55:57 - Call 6: "disponible"
    2025-02-21 01:55:58 - Call 7: "en mantenimiento"
    2025-02-21 01:55:59 - Call 8: "en mantenimiento"
    2025-02-21 01:56:00 - Call 9: "disponible"
    2025-02-21 01:56:04 - Call 10: "indispuesto"
    2025-02-21 01:56:05 - Fin Experimento
   ```
4. Realizar el análisis de los demás logs (el `logger.log` almacena los mensajes error reportados por el monitor) para comprobar que se ha detectado la/las falla/s.
