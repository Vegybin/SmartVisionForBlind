import os
add_dll_dir = getattr(os, "add_dll_directory", None)
vipsbin = r"c:\vips-dev-8.7\bin"  # LibVIPS binary dir
if callable(add_dll_dir):
    add_dll_dir(vipsbin)
else:
    os.environ["PATH"] = os.pathsep.join((vipsbin, os.environ["PATH"]))
from transformers import AutoModelForCausalLM
from PIL import Image
 
# Initialize the model
model = AutoModelForCausalLM.from_pretrained(
    "vikhyatk/moondream2",
    revision="2025-01-09",
    trust_remote_code=True,
    device_map={"": "cuda"}
)
 
# Load your image
image = Image.open("rabbit.png")
 
# 1. Image Captioning
print("Short caption:")
print(model.caption(image, length="short")["caption"])
 
print("\nDetailed caption:")
for t in model.caption(image, length="normal", stream=True)["caption"]:
    print(t, end="", flush=True)
 
# 2. Visual Question Answering
print("\nAsking questions about the image:")
print(model.query(image, "How many people are in the image?")["answer"])
 
# 3. Object Detection
print("\nDetecting objects:")
objects = model.detect(image, "face")["objects"]
print(f"Found {len(objects)} face(s)")
 
# 4. Visual Pointing
print("\nLocating objects:")
points = model.point(image, "person")["points"]
print(f"Found {len(points)} person(s)")