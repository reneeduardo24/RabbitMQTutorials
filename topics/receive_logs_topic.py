#!/usr/bin/env python
import pika # Cliente para RabbitMQ
import sys

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)

channel = connection.channel() # Via por la que se envian y reciben los mensajes

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare('', exclusive=True) # Declara una cola temporal, que se borra cuando se cierra la conexión
queue_name = result.method.queue

binding_keys = sys.argv[1:] # python receive_log_topic.py "kern.*" "*.critical"

if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange='topic_logs', # Origen de los mensajes que se van a recibir
        queue=queue_name, # Cola a la que se van a enviar los mensajes
        routing_key=binding_key # Clave de enrutamiento para filtrar los mensajes que se van a recibir
    )

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")

channel.basic_consume( # Registra este consumidor sobre la cola
    queue=queue_name,
    on_message_callback=callback, # Indica qué función ejecutar cuando llegue un mensaje.
    auto_ack=True # Marca el mensaje como recibido
)

channel.start_consuming() # Se queda a la espera de mensajes nuevos