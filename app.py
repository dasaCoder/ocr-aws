# from flask import Flask, render_template, make_response
# import os
# import time
# from PIL import Image
# import pytesseract
# import json
# import requests

# app = Flask(__name__)

# @app.route('/')
# def index():
#  url='https://docs.unity3d.com/Packages/com.unity.textmeshpro@3.2/manual/images/TMP_RichTextLineIndent.png'
#  image = Image.open(requests.get(url, stream=True).raw)
#  context = {'content' : pytesseract.image_to_string(image)}
#  return context

# if __name__ == '__main__':
#     app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

# app.py

from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
import json
import requests
from flask_cors import CORS, cross_origin
import cv2
import numpy as np

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return "Hello, World!"

@app.route('/ocr', methods=["POST"])
def index():
 if request.files.get("image") is None:
    return {'error': 'Image is missing'}
#  url='https://docs.unity3d.com/Packages/com.unity.textmeshpro@3.2/manual/images/TMP_RichTextLineIndent.png'
#  image = Image.open(requests.get(url, stream=True).raw)
 image = Image.open(request.files["image"])
 context = {'content' : pytesseract.image_to_string(image)}
 return context

@app.route('/ocr/optimized', methods=["POST"])
def ocrMapping():
    if "image" not in request.files:
        return jsonify({"error": "Image is missing"}), 400

    image_file = request.files["image"]
    
    # Perform input validation - Check if it's a valid image file

    # Preprocess the image
    image = Image.open(image_file)
    image = image.resize((800, 600))  # Resize to a lower resolution
    image = image.convert('L')  # Convert to grayscale
    # image = cv2.cvtColor(np.array(image), cv2.COLOR_GRAY2BGR)  # Convert back to RGB (for compatibility with pytesseract)

    image_np = np.array(image)
    # Apply denoising
    image_np = cv2.GaussianBlur(image_np, (5, 5), 0)

    # Thresholding
    _, image_np = cv2.threshold(image_np, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Perform OCR
    context = {"content": pytesseract.image_to_string(image_np)}

    return jsonify(context), 200
