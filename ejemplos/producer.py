#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()

channel.exchange_declare(exchange='monitor', exchange_type='direct')

message = 'respaldo'
channel.basic_publish(exchange='monitor', routing_key='healthcheck', body=message)
print(f" [x] Sent {message}")
