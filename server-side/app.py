from flask import Flask, request, Response
import pyttsx3
import io
from PIL import Image
from flask_cors import CORS
import random
import os
import image_stuff

app = Flask(__name__)
CORS(app)

current_caption = ""


@app.route('/process-image', methods=['POST'])
def process_image():
    global current_caption

    # Get the image file from the request
    file = request.files.get('image')
    if not file:
        return {"error": "No image provided"}, 400

    # Convert the uploaded image to a PIL Image
    image = Image.open(io.BytesIO(file.read())).convert("RGB")  # Convert to RGB format

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
    app.run(host="0.0.0.0")
