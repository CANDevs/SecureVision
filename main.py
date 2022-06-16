from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import hashlib
from flask_cors import CORS
from API.modelAPI import model_bp
from API.dataAPI import data_bp

app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SecureVision.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "GRd2Gmxh8o"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(300), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


CORS(app)
app.register_blueprint(model_bp)
app.register_blueprint(data_bp)

@app.route('/')
def home():
    if "user" in session:
        user = session["user"]
        title = f'Secure Vision - { user }'
        return render_template('index.html', title=title)
    else:
        flash("You need to login first")
        return redirect(url_for('login'))

@app.route('/compare')
def compare():
    if "user" in session:
        title = "Secure Vision - Compare Models"
        return render_template('compare.html', title=title)
    else:
        flash("You need to login first")
        return redirect(url_for('login'))
    

@app.route('/about')
def about_us():
    if "user" in session:
        title = "Secure Vision - About Us"
        return render_template('about.html',title=title)
    else:
        flash("You need to login first")
        return redirect(url_for('login'))

@app.route('/login',methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user_name = request.form['uname']
        password = request.form['password']
        password = hashlib.sha256(password.encode('utf-8'))
        password = password.hexdigest()
        res = User.query.filter_by(username=user_name, password=password).first()
        if res:
            session['user'] = user_name
            flash("Login Successful")
            return redirect(url_for('home'))
        else:
            title = "Secure Vision - Login"
            flash("Invalid Credentials")
            return render_template('login.html', title=title)
    else:
        if "user" in session:
            user = session["user"]
            title = f'Secure Vision - { user }'
            return redirect(url_for('home'))
        title = "Secure Vision - Login"
        return render_template('login.html', title=title)

@app.route('/logout')
def logout():
    flash("You have beed logged out!")
    session.pop("user", None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)