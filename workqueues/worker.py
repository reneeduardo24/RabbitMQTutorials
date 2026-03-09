#!/usr/bin/env python
import pika #Cliente para RabbitMQ
import time

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel() #Via por la que se envian y reciben los mensajes

channel.queue_declare(queue='task_queue', durable=True) #Asegura que la cola exista

print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag) # elimina el mensaje de la cola

channel.basic_qos(prefetch_count=1) # Fair dispatch
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming() #Inicia el consumo de mensajes, se queda a la espera de mensajes nuevos