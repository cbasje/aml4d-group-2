import os
import json
import requests

API_IMAGE_CLASSIFICATION_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"  # Image classification
API_OBJECT_DETECTION_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"  # Object detection

API_TOKEN = os.environ['API_TOKEN']
headers = {"Authorization": f'Bearer {API_TOKEN}'}


def request(api_url, data):
  response = requests.request("POST", api_url, headers=headers, data=data)
  return json.loads(response.content.decode("utf-8"))
