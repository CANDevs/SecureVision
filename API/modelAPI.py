from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from API.util import predict, save_map, image_loader
import base64

api_bp = Blueprint('modelapi',__name__)
api_model = Api(api_bp)
parser = reqparse.RequestParser()
parser.add_argument('model')
parser.add_argument('image')

class Model(Resource):
    def post(self):
        args = parser.parse_args()
        print(args)
        with open(args['image'], "rb") as imageFile:
            str_byte = base64.b64encode(imageFile.read())
        image = image_loader(str_byte)
        model = args['model']

        pred_map, pred_cnt, device, pred_time = predict(image, model)
        save_map(pred_map)
        res = {
            'pred_cnt': pred_cnt,
            'pred_time': pred_time,
            'device': device
        }
        return res, 200
api_model.add_resource(Model, '/predict')