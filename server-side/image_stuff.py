from transformers import AutoModelForCausalLM
from PIL import Image
 
model = AutoModelForCausalLM.from_pretrained(
    "vikhyatk/moondream2",
    revision="2025-01-09",
    trust_remote_code=True,
    device_map={"": "cuda"}
)

def get_all_objects(path):
    image = Image.open("rabbit.png")
    print(model.query(image, "List all the objects in the image?")["answer"])

get_all_objects("rabbit.png")
