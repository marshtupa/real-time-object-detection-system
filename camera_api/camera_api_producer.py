from kafka import KafkaProducer
import time
import sys
import cv2

input_topic = "distributed-video-input"
producer = KafkaProducer(bootstrap_servers='localhost:9092')


def publish_camera():
    camera = cv2.VideoCapture(0)
    try:
        while True:
            success, frame = camera.read()
            is_success, im_buf_arr = cv2.imencode(".jpg", frame)
            byte_im = im_buf_arr.tobytes()
            producer.send(input_topic, byte_im)
            time.sleep(3)
    except:
        camera.release()
        print("\nExiting.")
        sys.exit(1)


if __name__ == "__main__":
    print("Start publish camera")
    publish_camera()
