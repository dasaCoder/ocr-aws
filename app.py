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

from flask import Flask, request
from PIL import Image
import pytesseract
import json
import requests
from flask_cors import CORS, cross_origin

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
