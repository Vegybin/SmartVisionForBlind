from transformers import AutoModelForCausalLM
from PIL import Image
 
model = AutoModelForCausalLM.from_pretrained(
    "vikhyatk/moondream2",
    revision="2025-01-09",
    trust_remote_code=True,
    device_map={"": "cuda"}
)

def get_caption(path):
    image = Image.open(path)
    return model.caption(image, length="short")["caption"]
