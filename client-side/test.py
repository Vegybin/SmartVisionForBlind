import requests
import pygame
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "http://"+os.getenv("SERVER_IP")+":5000"

def play_audio(response):
    with open("response_audio.mp3", "wb") as f:
        f.write(response.content)
    
    pygame.mixer.init()
    pygame.mixer.music.load("response_audio.mp3")
    pygame.mixer.music.play()

def test_identify_face(image_path):
    url = f"{BASE_URL}/identify-face"
    files = {"image": open(image_path, "rb")}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        play_audio(response)
    else:
        print("Error:", response.json())

if __name__ == "__main__":
    test_identify_face("GroupPhoto.jpg")
