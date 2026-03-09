#!/usr/bin/env python
import pika # Cliente para RabbitMQ

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel() # Via por la que se envian y reciben los mensajes

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True) # Se eliminara la cola cuando la conexion se cierre

queue_name = result.method.queue # Guarda el nombre de la cola creada por RabbitMQ

channel.queue_bind(
    exchange='logs', # Origen de los mensajes que se van a recibir
    queue=queue_name
)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {body}")

channel.basic_consume( # Registra este consumidor sobre la cola
    queue=queue_name,
    on_message_callback=callback, # Indica qué función ejecutar cuando llegue un mensaje.
    auto_ack=True # Marca el mensaje como recibido
)

channel.start_consuming() # Se queda a la espera de mensajes nuevos