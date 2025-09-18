import os
import pika
import time
import psutil
import json

RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")

connection = pika.BlockingConnection(pika.ConnectionParameters(RABBIT_HOST))
channel = connection.channel()
channel.queue_declare(queue='system_load')

while True:
    load1, load5, load15 = psutil.getloadavg()
    cpu_percent = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    data = {
        'load1': load1,
        'load5': load5,
        'load15': load15,
        'cpu_percent': cpu_percent,
        'memory_percent': mem.percent
    }
    channel.basic_publish(exchange='', routing_key='system_load', body=json.dumps(data))
    print("Sent:", data)
    time.sleep(1)
