import sys,pika,os
from moviepy.editor import VideoFileClip
import json

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("PUBSUB_HOSTNAME"), port=5672))
    channel = connection.channel()

    channel.queue_declare(queue='extract_sound', durable=True)

    def send_message_to_pubsub(msg:str):
        try:
            channel.basic_publish(
                exchange='',
                routing_key="new_file",
                body=msg,
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent
                ))
        except Exception as err:
            raise(err)

    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        video = VideoFileClip(f"/app/bucket/{body.decode()}")
        filename, _ = os.path.splitext(f"/app/bucket/{body.decode()}")
        video.audio.write_audiofile(f"{filename}.mp3")

        send_message_to_pubsub(json.dumps({"type":"sound", "file_name":f"{filename}.mp3"}))


    channel.basic_consume(queue='extract_sound', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)