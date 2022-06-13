from flask import Blueprint, request, json, Flask
import os
from flask_restful import Api

data_bp = Blueprint('data',__name__)
data_api = Api(data_bp)


@data_bp.route('/images/', methods=['GET'])
def get_images():
    dataset = request.args.get("dataset") or "SHHB"

    folder = 'static/datasets/' + dataset
    imgs = os.listdir(folder)

    data = [{"path": folder + "/" + file, "name": file.replace(".jpg", "")} for file in imgs if file.endswith(".jpg")]
    data = data[:10] #return only the first 10 images

    return Flask.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )


@data_bp.route('/groundtruth/', methods=['GET'])
def get_all_groundtruth():
    dataset = request.args.get("dataset") or "NPWU-CROWD"

    folder = 'static/datasets/' + dataset
    imgs = os.listdir(folder)
    imgs = imgs[:5]

    data = {}
    for file in imgs:
        if file.endswith(".json"):
            filepath = folder + "/" + file
            f = open(filepath, "r")
            j = json.load(f)
            
            num = None

            if "human_num" in j:
                num = j["human_num"]

            if num == None and num != 0:
                num = "Non Disponibile"

            data[filepath] = num

    return Flask.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )


@data_bp.route('/groundtruth/<name>/', methods=['GET'])
def get_groundtruth(name):

    dataset = request.args.get("dataset") or "NPWU-CROWD"

    filepath = 'static/datasets/' + dataset + '/' + name + '.json'
    f = open(filepath, "r")
    j = json.load(f)

    return Flask.response_class(
        response=json.dumps(j),
        status=200,
        mimetype='application/json'
    )