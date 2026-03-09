#!/usr/bin/env python
import pika #Cliente para RabbitMQ
import sys

connection = pika.BlockingConnection( 
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel() #Via por la que se envian y reciben los mensajes

channel.queue_declare(queue='task_queue', durable=True) 

message = ' '.join(sys.argv[1:]) or "Hello World!"
# python new_task.py First message...

channel.basic_publish( #Metodo con el que RabbitMQ recibe el mensaje
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.DeliveryMode.Persistent #Hace que el mensaje se guarde en disco, para que no se pierda si RabbitMQ se cae
    )
)

print(f" [x] Sent {message}") #Imprime el mensaje enviado

connection.close() #Cierra la conexion con RabbitMQ