import os
import asyncio
import logging
from time import sleep

import pika
import random
from fastapi import FastAPI

instancia = os.getenv("API_INSTANCIA", "principal")
rabbitmq_host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
puerto = os.getenv("API_PUERTO", "8090")

logging.basicConfig(
    level=logging.DEBUG,
    format='%(name)s|[%(levelname)s]|%(asctime)s|%(message)s',
    handlers=[
        logging.FileHandler(f"logs/api-consulta-{instancia}.log", mode="w"),
        logging.StreamHandler()
    ]
)

# Set pika logger to WARNING level to suppress INFO logs
logging.getLogger("pika").setLevel(logging.WARNING)


app = FastAPI()

mock_statuses = ['disponible', 'indispuesto', 'en mantenimiento']

def publicar_estado():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    channel.exchange_declare(exchange='monitor', exchange_type='direct')

    properties = pika.BasicProperties(headers={'log_level': 'DEBUG'})
    channel.basic_publish(exchange='monitor', routing_key='healthcheck', body=instancia, properties=properties)
    logging.debug(f"[API-Consulta-{instancia.capitalize()}] Sent {instancia}")


async def publicar_estado_periodicamente():
    while True:
        publicar_estado()
        await asyncio.sleep(1)


@app.on_event("startup")
async def startup_event():
    global background_task
    background_task = asyncio.create_task(publicar_estado_periodicamente())


@app.get('/consulta', response_model=str)
async def consulta():
    status = random.choice(mock_statuses)
    if status == 'indispuesto':
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            logging.error("Background task cancelled")

        sleep(3)
        await startup_event()

    return status

@app.get("/health")
async def health():
    return "ok"

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=int(puerto))