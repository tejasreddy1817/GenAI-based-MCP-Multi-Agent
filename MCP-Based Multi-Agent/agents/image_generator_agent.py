"""
ImageGeneratorAgent: generates image from text using Hugging Face Stable Diffusion.
"""
import os
import requests
from io import BytesIO
from PIL import Image

class ImageGeneratorAgent:
    def __init__(self):
        
        self.hf_token = os.getenv("HF_API_TOKEN")

    def run(self, prompt: str) -> str:
        if not self.hf_token:
            raise ValueError("No API key found! Set HF_API_TOKEN in .env file.")
        return self._generate_with_huggingface(prompt)

    def _generate_with_huggingface(self, prompt: str) -> str:
        API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
        headers = {"Authorization": f"Bearer {self.hf_token}"}
        payload = {"inputs": prompt}

        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"HuggingFace API failed: {response.text}")

        # save the image returned by HF API
        img_path = "generated_image.png"
        image = Image.open(BytesIO(response.content))
        image.save(img_path)
        return img_path
