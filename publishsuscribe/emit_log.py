#!/usr/bin/env python
import pika #Cliente para RabbitMQ
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel() #Via por la que se envian y reciben los mensajes

channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
# python emit_log.py First message...

channel.basic_publish(
    exchange='logs', #Mensaje va a ser enviado a este exchange
    routing_key='', #No se necesita una routing key para el tipo de exchange 'fanout'
    body=message #El mensaje que se va a enviar
)

print(f" [x] Sent {message}")

connection.close() #Cierra la conexion con RabbitMQ