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

1. Se deben configurar las variables de entorno: Crear un archivo `.env` dentro de la carpeta principal y se deben agregar las siguientes variables: 
    ```
    DIRECTORIO_LOGS=logs
    URL_API_CONSULTA=host.docker.internal/inventario
    ```

2. Se debe ejecutar el siguiente comando para levantar los micro-servicios y ejecutar el experimento: 
    ```
    docker compose up
    ```
3. Esperar a que se ejecuten las pruebas del experimento, deberá aparecer un log con un mensaje indicando que la prueba ha finalizado.
4. Verificar los logs en el directorio `logs`