from flask import Blueprint
from flask_restful import Resource, Api, reqparse
from API.util import predict, save_map, image_loader, get_frame
import base64
from PIL import Image

model_bp = Blueprint('modelapi', __name__)
api_model = Api(model_bp)
parser = reqparse.RequestParser()
parser.add_argument('model')
parser.add_argument('image')
parser.add_argument('video')
parser.add_argument('video_url')
parser.add_argument('secs')
parser.add_argument('new_request')

gen : any = None
class Model_Image(Resource):
    def post(self):
        args = parser.parse_args()
        with open("."+args['image'], "rb") as imageFile:
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


class Model_Video(Resource):


    def post(self):
        global gen
        args = parser.parse_args()
        model = args['model']
        hasFrames = True
        if (args['new_request']) == 'True':
            gen = get_frame(args['video_url'], args['secs'])

        hasFrames, image = next(gen)
        image = Image.fromarray(image)
        pred_map, pred_cnt, device, pred_time = predict(image, model)
        save_map(pred_map)
        res = {
            'pred_cnt': pred_cnt,
            'pred_time': pred_time,
            'device': device,
            'next_frame': True,
            'new_request': False,
        }
        return res, 200


api_model.add_resource(Model_Image, '/predict')
api_model.add_resource(Model_Video, '/predict_video')
