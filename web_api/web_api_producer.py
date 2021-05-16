from flask import Flask, render_template, request
from kafka import KafkaProducer
from PIL import Image
import requests
import io

app = Flask(__name__)

input_topic = "distributed-video-input"
producer = KafkaProducer(bootstrap_servers='localhost:9092')


def load_image_from_url():
    url = request.args.get("url")
    downloaded_image = requests.get(url)
    return io.BytesIO(downloaded_image.content)


def prepare_result_image(result_img):
    buffer = io.BytesIO()
    result_img.save(buffer, 'JPEG')
    return buffer.getvalue()


def open_rgb_image(source):
    try:
        image = Image.open(source)
        rgb_image = image.convert('RGB')
        return rgb_image
    except Exception as e:
        print(e)
        return render_template("failure.html")


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/detect", methods=['POST'])
def upload():
    rgb_image = open_rgb_image(request.files['file'].stream)
    producer.send(input_topic, prepare_result_image(rgb_image))
    return "Image was sent to kafka"


@app.route("/detect", methods=['GET'])
def upload_from_url():
    rgb_image = open_rgb_image(load_image_from_url())
    producer.send(input_topic, prepare_result_image(rgb_image))
    return "Image was sent to kafka"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
