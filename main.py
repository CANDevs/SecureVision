from flask import Flask
from API.modelAPI import model_bp
from API.dataAPI import data_bp
from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1


CORS(app)
app.register_blueprint(model_bp)
app.register_blueprint(data_bp)


@app.route('/')
def home():
    title = 'Secure Vision'
    return render_template('index.html', title=title)

@app.route('/compare')
def compare():
    title = "Secure Vision - Compare Models"
    return render_template('compare.html', title=title)

@app.route('/about')
def about_us():
    title = "Secure Vision - About Us"
    return render_template('about.html',title=title)


if __name__ == '__main__':
    app.run(debug=True)