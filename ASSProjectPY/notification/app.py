import pika
import json
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)

def send_notification(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')
    channel.basic_publish(exchange='', routing_key='notifications', body=json.dumps(message))
    connection.close()


@app.route('/notify', methods=['POST'])
def notify():
    data = request.json
    send_notification(data)
    return jsonify({"status": "Notification sent!"}), 200

def listen_for_notifications():
    def callback(ch, method, properties, body):
        print(f"Notification received: {body}")

    connection_parameters = pika.ConnectionParameters(
        host='rabbitmq',
        retry_delay=5,
        connection_attempts=10
    )

    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='notifications')
    channel.basic_consume(queue='notifications', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    
thread = threading.Thread(target=listen_for_notifications)
thread.start()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)