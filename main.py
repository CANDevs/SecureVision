from flask import Flask
from flask_restful import Resource, Api
import os
from flask import Flask, render_template, request, json
from numpy import result_type
from flask_cors import CORS
from API.util import predict, save_map, image_loader
import base64
app = Flask(__name__)
api = Api(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
CORS(app)


@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route('/')
def home():
    title = 'Crowd Counting DEMO'
    return render_template('index.html', title=title)


@app.route('/predict', methods=['POST'])
def predict_page():
    with open("./static/datasets/SHHB/2.jpg", "rb") as imageFile:
        str_byte = base64.b64encode(imageFile.read())
    dataset = "SHHB"
    image = image_loader(str_byte)
    model = request.json['model']

    pred_map, pred_cnt, device, pred_time = predict(dataset, image, model)
    save_map(pred_map)
    res = {
        'pred_cnt': pred_cnt,
        'pred_time': pred_time,
        'device': device
    }
    return json.dumps(res)

if __name__ == '__main__':
    app.run(debug=True)