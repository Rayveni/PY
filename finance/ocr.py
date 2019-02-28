from pytesseract import image_to_string
import requests
from PIL import Image,ImageEnhance,ImageFilter
from io import BytesIO
import numpy as np

class ocr:
    @staticmethod
    def download_image(url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        return img

    def recognize_text(img):
        file = BytesIO()
        img=PIL.ImageEnhance.Sharpness (img.convert('RGB'))
        img_converted = img.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(img_converted)
        img_converted=enhancer.enhance(2)
        
        img_converted=img_converted.convert('1')
        img_converted.save(file, 'png')
        img_converted= Image.open(file)
        return image_to_string(img_converted,lang='eng')