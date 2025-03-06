from flask import Flask, request, Response
import pyttsx3
import cv2
# from flask_cors import CORS
import numpy as np
import random
import os
import image_stuff

app = Flask(__name__)
# CORS(app)

current_caption = ""


@app.route('/process-image', methods=['POST'])
def process_image():
    global current_caption

    # Get the image file from the request
    file = request.files.get('image')
    if not file:
        return {"error": "No image provided"}, 400

    # Convert the uploaded image to a NumPy array and decode it using OpenCV
    file_bytes = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # OpenCV loads images in BGR format

    # Process the image using YOLO
    current_caption = image_stuff.get_caption(image)

    return {"message": "true"}


@app.route('/objects-now', methods=['GET'])
def objects_now():
    global current_caption
    engine = pyttsx3.init()
    rand_int = random.randint(0,999999)
    engine.save_to_file(current_caption, "output"+rand_int+".mp3")
    engine.runAndWait()

    # Read the saved file and stream it
    with open("output"+rand_int+".mp3", "rb") as f:
        audio_data = f.read()
    os.remove("output"+rand_int+".mp3")

    return Response(audio_data, mimetype="audio/mpeg")


if __name__ == '__main__':
    app.run()
