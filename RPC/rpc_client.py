#!/usr/bin/env python
import pika # Cliente para RabbitMQ
import uuid

class FibonacciRpcClient(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel() # Via por la que se envian y reciben los mensajes

        result = self.channel.queue_declare(queue='', exclusive=True) # Declara una cola temporal, que se borra cuando se cierra la conexión
        self.callback_queue = result.method.queue # Guarda el nombre de la cola creada por RabbitMQ

        self.channel.basic_consume( # Registra este consumidor sobre la cola
            queue=self.callback_queue,
            on_message_callback=self.on_response, # Cuando llegue un mensaje de respuesta, RabbitMQ ejecutará el método on_response.
            auto_ack=True # Marca el mensaje como recibido
        )

        self.response = None # Variable para almacenar la respuesta del servidor
        self.corr_id = None # Variable para almacenar el correlation_id

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n):
        self.response = None 
        self.corr_id = str(uuid.uuid4()) # Genera un correlation_id único para esta solicitud

        self.channel.basic_publish( # Envia la solicitud RPC al servidor
            exchange='', # exchange por defecto
            routing_key='rpc_queue', # Nombre de la cola donde se va a enviar la solicitud
            properties=pika.BasicProperties( # Creacion de las propiedades del mensaje de solicitud
                reply_to=self.callback_queue, # Indica al servidor a qué cola enviar la respuesta
                correlation_id=self.corr_id, 
            ),
            body=str(n)
        )

        while self.response is None: # El cliente se queda esperando hasta que la respuesta válida sea recibida.
            self.connection.process_data_events(time_limit=None)

        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print(" [x] Requesting fib(30)")
response = fibonacci_rpc.call(30)
print(f" [.] Got {response}")