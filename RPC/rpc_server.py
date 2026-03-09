#!/usr/bin/env python
import pika # Cliente para RabbitMQ

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel() # Via por la que se envian y reciben los mensajes

channel.queue_declare(queue='rpc_queue') # Esta cola será la cola donde los clientes enviarán sus solicitudes RPC

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def on_request(ch, method, props, body):
    n = int(body)
    print(f" [.] fib({n})")

    response = fib(n)

    ch.basic_publish( # Envio de respuesta al cliente
        exchange='', # exchange por defecto
        routing_key=props.reply_to, # Nombre de la cola donde se va a recibir la respuesta
        properties=pika.BasicProperties( # Creacion de las propiedades del mensaje de respuesta
            correlation_id=props.correlation_id # Identificar la respuesta con la solicitud original usando correlation_id
        ),
        body=str(response)
    )

    ch.basic_ack(delivery_tag=method.delivery_tag) # Marca el mensaje como procesado, para que RabbitMQ lo elimine de la cola

channel.basic_qos(prefetch_count=1) # Limita a un mensaje no reconocido por consumidor a la vez
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request) # Registra la función on_request como callback para los mensajes que lleguen a la cola 'rpc_queue'

print(" [x] Awaiting RPC requests")
channel.start_consuming() # Desde aquí el servidor queda escuchando peticiones RPC indefinidamente.