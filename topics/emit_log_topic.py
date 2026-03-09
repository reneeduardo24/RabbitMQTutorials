#!/usr/bin/env python
import pika # Cliente para RabbitMQ
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel() # Via por la que se envian y reciben los mensajes

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'

message = ' '.join(sys.argv[2:]) or 'Hello World!'
# python emit_log_topic.py kern.critical "A critical kernel error"

channel.basic_publish( # Metodo con el que RabbitMQ envia el mensaje
    exchange='topic_logs',
    routing_key=routing_key,
    body=message
)

print(f" [x] Sent {routing_key}:{message}")

connection.close()