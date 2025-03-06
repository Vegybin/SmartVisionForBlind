from flask import Flask, request, Response
import io
from PIL import Image
from flask_cors import CORS
import random
import os
import image_stuff
from gtts import gTTS

app = Flask(__name__)
CORS(app)



@app.route('/caption-image', methods=['POST'])
def process_image():

    # Get the image file from the request
    file = request.files.get('image')
    if not file:
        return {"error": "No image provided"}, 400

    # Convert the uploaded image to a PIL Image
    image = Image.open(io.BytesIO(file.read())).convert("RGB")  # Convert to RGB format

    # Process the image using YOLO
    current_caption = image_stuff.get_caption(image)
    tts = gTTS(text=current_caption, lang='en')
    rand_int = str(random.randint(0,999999))
    tts.save("output"+rand_int+".mp3")

    # Read the saved file and stream it
    with open("output"+rand_int+".mp3", "rb") as f:
        audio_data = f.read()
    os.remove("output"+rand_int+".mp3")

    return Response(audio_data, mimetype="audio/mpeg")


if __name__ == '__main__':
    app.run(host="0.0.0.0")
