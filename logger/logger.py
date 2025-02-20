#!/usr/bin/env python
import logging
from enum import StrEnum, auto

import pika


class LogLevelType(StrEnum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()

log_level_map = {
    'DEBUG': logging.debug,
    'INFO': logging.info,
    'WARNING': logging.warning,
    'ERROR': logging.error,
    'CRITICAL': logging.critical
}


logging.basicConfig(
    level=logging.INFO,
    format='%(name)s|[%(levelname)s]|%(asctime)s|%(message)s',
    handlers=[
        logging.FileHandler("logs/logger.log"),
        logging.StreamHandler()
    ]
)


connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='monitor', exchange_type='direct')

result = channel.queue_declare(queue='error_report', exclusive=True)
channel.queue_bind(exchange='monitor', queue='error_report',routing_key='error')

logging.info('[Logger] Waiting for logs.')

def callback(ch, method, properties, body):
    log_level = properties.headers.get('log_level', 'INFO') if properties and properties.headers else 'INFO'
    log_func = log_level_map.get(log_level, logging.info)
    log_func(body)

channel.basic_consume(
    queue='error_report', on_message_callback=callback, auto_ack=True)

channel.start_consuming()