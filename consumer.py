import pika, json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"Load1: {data['load1']:.2f}, Load5: {data['load5']:.2f}, "
          f"Load15: {data['load15']:.2f}, CPU: {data['cpu_percent']}%, "
          f"MEM: {data['memory_percent']}%")

connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.0.131')   # RabbitMQ host IP
)
channel = connection.channel()
channel.queue_declare(queue='system_load')

channel.basic_consume(queue='system_load', on_message_callback=callback, auto_ack=True)
print(" [*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
