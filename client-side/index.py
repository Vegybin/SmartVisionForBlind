import cv2
from picamera2 import Picamera2
import requests
from dotenv import load_dotenv
import os

load_dotenv()
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"size": (1138,640)})
picam2.configure(config)
picam2.start()
frame = picam2.capture_array()
frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
cv2.imwrite("myImage.png", frame)

url = "http://"+os.getenv("SERVER_IP")+":5000/caption-image"
files = {"image": open("myImage.png", "rb")}

response = requests.post(url, files=files)

if response.status_code == 200:
    with open("output.mp3", "wb") as f:
        f.write(response.content)
    print("Audio file saved as output.mp3")
else:
    print("Error:", response.json())
