from io import BytesIO
from base64 import encodebytes

from flask import Flask, request, jsonify
from flask_cors import CORS

from chat import process


app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    content = request.json
    print("Got:", content)

    msg = content["msg"]
    response, image = process(msg)
    print("Out:", response)

    # Create a BytesIO object to hold the image data
    img_io = BytesIO()
    image.save(img_io, format='JPEG')
    img_io.seek(0)
    encoded_img = encodebytes(img_io.getvalue()).decode('ascii')  # encode as base64

    return { "msg": response, "img": encoded_img }

