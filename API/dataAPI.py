from flask import Blueprint,json, Flask
import os
from flask_restful import Resource, Api, reqparse


data_bp = Blueprint('data',__name__)
data_api = Api(data_bp)
parser = reqparse.RequestParser()
parser.add_argument("dataset")

class GetImages(Resource):
    def get(self):
        args = parser.parse_args()
        dataset = args["dataset"]
        folder = 'static/datasets/' + dataset
        imgs = os.listdir(folder)

        data = [{"path": folder + "/" + file, "name": file.replace(".jpg", "")} for file in imgs if file.endswith(".jpg")]
        data = data[:10]

        return Flask.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
        )

class GetGroundTruth(Resource):
    def get(self, name):
        args = parser.parse_args()
        dataset = args["dataset"]
        filepath = 'static/datasets/' + dataset + '/' + name + '.json'
        f = open(filepath, "r")
        j = json.load(f)

        return Flask.response_class(
        response=json.dumps(j),
        status=200,
        mimetype='application/json'
        )

class GetAllGroundTruth(Resource):
    def get(self):
        args = parser.parse_args()
        dataset = args["dataset"]
        folder = 'static/datasets/' + dataset
        imgs = os.listdir(folder)

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

data_api.add_resource(GetImages, "/images/")
data_api.add_resource(GetAllGroundTruth, "/groundtruth/")
data_api.add_resource(GetGroundTruth, "/groundtruth/<name>/")