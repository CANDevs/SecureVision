from flask import Flask
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

if __name__ == '__main__':
    app.run(debug=True)