from flask import Flask, request
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
    response = process(msg)
    print("Out:", response)

    return { "msg": response }
