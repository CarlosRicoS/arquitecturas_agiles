#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='monitor', exchange_type='direct')

result = channel.queue_declare(queue='error_report', exclusive=True)
channel.queue_bind(exchange='monitor', queue='error_report',routing_key='error')

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {body}")

channel.basic_consume(
    queue='error_report', on_message_callback=callback, auto_ack=True)

channel.start_consuming()