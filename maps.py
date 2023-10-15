import requests
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
from PIL import Image
import numpy as np

GOOGLE_MAPS_API_KEY = "AIzaSyDBGZsGvmNASpvgMRwQ2cpmz8tIgsiwFR0"


def get_location_image_with_key(user_location, api_key, signature=None):
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    params = {
        "center": user_location,
        "zoom": 20,
        "size": "600x300",
        "maptype": "satellite",
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


def convert_2d_image_to_3d(image):
    """Converts a 2D image to a 3D image by adding a dummy channel dimension.

    Args:
        image: A 2D NumPy array representing the image.

    Returns:
        A 3D NumPy array representing the image with a dummy channel dimension.
    """

    image = np.expand_dims(image, axis=2)
    return image


def get_building_area(user_location):
    image_path = get_location_image(user_location)
    image_path = get_location_image_with_key(user_location, api_key)

    if image_path:
        print(f"Location image saved as {image_path}")
    else:
        print("Failed to retrieve the location image.")
    

    # Open the local image file
    image = Image.open(image_path)
    mean = None
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    mean, std = processor.get_default_normalize()

    # Convert the 2D image to a 3D image.
    image_3d = convert_2d_image_to_3d(image)

    inputs = processor(images=image_3d, return_tensors="pt", mean=mean, std=std)
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

