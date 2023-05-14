from io import BytesIO
from base64 import encodebytes

from flask import Flask, request
from flask_cors import CORS

from chat_api import ask_GPT
from weather_forecast import visualize_forecast

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
    task, response = ask_GPT(msg)

    # Create a BytesIO object to hold the image data
    img_io = BytesIO()
    response["image"].save(img_io, format='JPEG')
    img_io.seek(0)
    encoded_img = encodebytes(img_io.getvalue()).decode('ascii')  # encode as base64
    response["image"] = encoded_img

    if "location" in response:
        forecast_image = visualize_forecast(response["location"])
        img_io = BytesIO()
        forecast_image.save(img_io, format='JPEG')
        img_io.seek(0)
        response["forecast_image"] = encodebytes(img_io.getvalue()).decode('ascii')  # encode as base64

    return {"task": task, "response": response}
