import requests
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image


GOOGLE_MAPS_API_KEY = "AIzaSyDBGZsGvmNASpvgMRwQ2cpmz8tIgsiwFR0"


def get_location_image_with_key(user_location, api_key, signature=None):
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    params = {
        "center": user_location,
        "zoom": 20,
        "size": "600x300",
        "maptype": "roadmap",
        "key": api_key,
    }

    if signature:
        params["signature"] = signature

    markers = ["color:blue|label:S|40.702147,-74.015794", "color:green|label:G|40.711614,-74.012318", "color:red|label:C|40.718217,-73.998284"]
    markers_str = "&".join(markers)
    url = f"{base_url}{markers_str}&" + "&".join([f"{k}={v}" for k, v in params.items()])

    response = requests.get(url)

    if response.status_code == 200:
        with open("location_map.png", "wb") as f:
            f.write(response.content)
        return "location_map.png"
    else:
        return None

# Replace 'YOUR_API_KEY' with your actual API key
api_key = GOOGLE_MAPS_API_KEY
    

def get_location_image(user_location=""):
    return get_location_image_with_key(user_location=user_location, 
                                       api_key=api_key)


API_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"
headers = {"Authorization": "Bearer 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"}


def get_building_area(user_location):
    image_path = get_location_image(user_location)
    image_path = get_location_image_with_key(user_location, api_key)

    if image_path:
        print(f"Location image saved as {image_path}")
    else:
        print("Failed to retrieve the location image.")
    

    # Open the local image file
    image = Image.open(image_path)

    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    # convert outputs (bounding boxes and class logits) to COCO API
    # let's only keep detections with score > 0.9
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs,
                                                      target_sizes=target_sizes, 
                                                      threshold=0.9)[0]

    for score, label, box in zip(results["scores"], results["labels"], 
                                 results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        print(
                f"Detected {model.config.id2label[label.item()]} with confidence "
                f"{round(score.item(), 3)} at location {box}"
    )
        
    return 42

