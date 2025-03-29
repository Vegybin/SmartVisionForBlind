import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = "http://"+os.getenv("SERVER_IP")+":5000"

def test_store_face(image_path, name):
    url = f"{BASE_URL}/store-face"
    files = {"image": open(image_path, "rb")}
    data = {"name": name}
    response = requests.post(url, files=files, data=data)
    print("Store Face Response:", response.json())

def test_identify_face(image_path):
    url = f"{BASE_URL}/identify-face"
    files = {"image": open(image_path, "rb")}
    response = requests.post(url, files=files)
    print("Identify Face Response:", response.json())

if __name__ == "__main__":
    test_store_face("BarrackObama.jpg", "Barrack Obama")
    test_identify_face("GroupPhoto.jpg")
