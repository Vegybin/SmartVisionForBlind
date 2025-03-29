from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import random
import os
import io
import image_stuff
import face_recognition
import psycopg2
import numpy as np
from gtts import gTTS
import speech_recognition as sr
from PIL import Image

app = Flask(__name__)
CORS(app)

# Database connection
conn = psycopg2.connect(
    dbname='face_db', user='postgres', password='firepaan', host='localhost', port='5432'
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS faces (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        embedding FLOAT8[] NOT NULL
    )
''')
conn.commit()

@app.route('/store-face', methods=['POST'])
def store_face():
    file = request.files.get('image')
    name = request.form.get('name')
    
    if not file or not name:
        return jsonify({"error": "Image and name are required"}), 400
    
    image = face_recognition.load_image_file(io.BytesIO(file.read()))
    face_encodings = face_recognition.face_encodings(image)
    
    if len(face_encodings) == 0:
        return jsonify({"error": "No face detected"}), 400
    
    embedding = face_encodings[0].tolist()
    cursor.execute("INSERT INTO faces (name, embedding) VALUES (%s, %s)", (name, embedding))
    conn.commit()
    
    return jsonify({"message": "Face stored successfully"})

@app.route('/identify-face', methods=['POST'])
def identify_face():
    file = request.files.get('image')
    
    if not file:
        return jsonify({"error": "Image is required"}), 400
    
    image = face_recognition.load_image_file(io.BytesIO(file.read()))
    unknown_encodings = face_recognition.face_encodings(image)
    
    if len(unknown_encodings) == 0:
        return jsonify({"error": "No face detected"}), 400
    
    cursor.execute("SELECT name, embedding FROM faces")
    stored_faces = cursor.fetchall()
    
    identified_faces = []
    threshold = 0.80  # 80% similarity threshold
    
    for unknown_encoding in unknown_encodings:
        for name, embedding in stored_faces:
            known_encoding = np.array(embedding, dtype=np.float64)
            similarity = 1 - np.linalg.norm(known_encoding - unknown_encoding)
            
            if similarity > threshold:
                identified_faces.append(name)
    
    return jsonify({"identified_faces": list(set(identified_faces))})


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


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    file = request.files.get('audio')
    if not file:
        return jsonify({"error": "No audio provided"}), 400

    recognizer = sr.Recognizer()

    with io.BytesIO(file.read()) as audio_file:
        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

            try:
                text = recognizer.recognize_google(audio_data)
                return jsonify({"text": text})
            except sr.UnknownValueError:
                return jsonify({"error": "Could not understand audio"}), 400
            except sr.RequestError:
                return jsonify({"error": "Could not request results from the speech recognition service"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0")
