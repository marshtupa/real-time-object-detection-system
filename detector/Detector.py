from kafka import KafkaConsumer, KafkaProducer
from Detectron2Client import Detectron2Client
from PIL import Image
import numpy
import io


input_topic = "distributed-video-input"
output_topic = "distributed-video-output"
consumer = KafkaConsumer(input_topic, bootstrap_servers=['192.168.0.100:9092'])
producer = KafkaProducer(bootstrap_servers='192.168.0.100:9092')

detector = Detectron2Client()


def image_to_bytes(image):
    buffer = io.BytesIO()
    image.save(buffer, 'JPEG')
    return buffer.getvalue()


def get_image_from_message(msg):
    try:
        image = Image.open(io.BytesIO(msg.value))
        return numpy.array(image)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    print("application is run")
    for msg in consumer:
        print("Image was received")
        image = get_image_from_message(msg)
        result_img = detector.inference(image)
        producer.send(output_topic, image_to_bytes(result_img))
        print("Image was sent to topic")

