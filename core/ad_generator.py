from diffusers import StableDiffusionPipeline
import torch
from PIL import Image, ImageDraw, ImageFont
import requests

class AdGenerator:
    def __init__(self):
        self.pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
        self.pipe = self.pipe.to("cuda")

    def generate(self, prompt: str, business: dict):
        # 1. Generate base image
        image = self.pipe(prompt).images[0]
        
        # 2. Add text overlay
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 40)
        draw.text((50, 50), business['ad_text'], fill="white", font=font)
        draw.text((50, 100), f"Call: {business['phone']}", fill="yellow", font=font)
        
        # 3. Save to IPFS
        image.save("ad.png")
        ipfs_hash = self.upload_to_ipfs("ad.png")
        
        return {
            "image": f"ipfs://{ipfs_hash}",
            "target": business['location'],
            "url": business['website']
        }
