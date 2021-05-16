from flask import Flask, Response, render_template
from kafka import KafkaConsumer

app = Flask(__name__)

output_topic = "distributed-video-output"

consumer = KafkaConsumer(
    output_topic,
    bootstrap_servers=['localhost:9092'])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed', methods=['GET'])
def video_feed():
    return Response(
        get_video_stream(), 
        mimetype='multipart/x-mixed-replace; boundary=frame')


def get_video_stream():
    for msg in consumer:
        print("Image was received")
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + msg.value + b'\r\n\r\n')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9090)
