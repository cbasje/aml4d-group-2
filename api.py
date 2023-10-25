import os
import json
import requests

# Define the Hugging Face API URLs for the two used models
API_IMAGE_CLASSIFICATION_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"  # Image classification
API_OBJECT_DETECTION_URL = "https://api-inference.huggingface.co/models/facebook/detr-resnet-50"  # Object detection


# Define the Hugging Face API token and 
API_TOKEN = os.environ['API_TOKEN']


# Define a reusable function to perform requests to the Hugging Face API
def request(api_url, data):
  headers = {"Authorization": f'Bearer {API_TOKEN}'}
  response = requests.request("POST", api_url, headers=headers, data=data)
  return json.loads(response.content.decode("utf-8"))
