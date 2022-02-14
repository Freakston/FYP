import json
from core.Utils.utils import rabConnect
from base64 import b64decode
class Fuzzer():
    def __init__(self) -> None:
        self.channel = rabConnect()
    
    def run(self, app):
        print("Implement run Fuzzing")

    def blob_consumer(ch, method, properties, message):
        try:
            decoded_message = json.loads(message.decode("utf-8"))
        except Exception as e:
            print(f"[Client error] failed trying to decode the message {e}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        blob = b64decode(decoded_message)
        print(f"Succesfully decoded the blob {blob}")

    def start_exploit_consumer(self):
        # Connect to the result queue - consumer
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(
            queue="task-queue", on_message_callback=blob_consumer)

        self.channel.start_consuming()


    

