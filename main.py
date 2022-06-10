from flask import Flask, request, json
import os
from API.modelAPI import api_bp
from flask import Flask, render_template
from flask_cors import CORS
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
CORS(app)
app.register_blueprint(api_bp)

@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


@app.route('/')
def home():
    title = 'Secure Vision'
    return render_template('index.html', title=title)

@app.route('/compare')
def compare():
    title = "Secure Vision - Compare Models"
    return render_template('compare.html', title=title)


@app.route('/images/', methods=['GET'])
def get_images():
    dataset = request.args.get("dataset") or "SHHB"
    model = request.args.get("model") or "AlexNet"

    folder = 'static/datasets/' + dataset
    imgs = os.listdir(folder)

    data = [{"path": folder + "/" + file, "name": file.replace(".jpg", "")} for file in imgs if file.endswith(".jpg")]
    data = data[:10] #return only the first 10 images

    return app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )


@app.route('/groundtruth/', methods=['GET'])
def get_all_groundtruth():
    dataset = request.args.get("dataset") or "NPWU-CROWD"
    model = request.args.get("model") or "AlexNet"

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

    return app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )


@app.route('/groundtruth/<name>/', methods=['GET'])
def get_groundtruth(name):

    dataset = request.args.get("dataset") or "NPWU-CROWD"
    model = request.args.get("model") or "AlexNet"

    filepath = 'static/datasets/' + dataset + '/' + name + '.json'
    f = open(filepath, "r")
    j = json.load(f)

    return app.response_class(
        response=json.dumps(j),
        status=200,
        mimetype='application/json'
    )


if __name__ == '__main__':
    app.run(debug=True)