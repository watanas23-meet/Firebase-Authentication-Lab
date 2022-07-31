from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyCz4TxQUGk3PPs96-oD4vOuX9DwmEyY7NM",
  "authDomain": "meettutorial-cda45.firebaseapp.com",
  "projectId": "meettutorial-cda45",
  "storageBucket": "meettutorial-cda45.appspot.com",
  "messagingSenderId": "314514460185",
  "appId": "1:314514460185:web:fc5e02feb1e45076ae6488",
  "databaseURL": ""
};


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = user = auth.sign_in_with_email_and_password(email, password)
            return(redirect('add_tweet'))
        except:
            error="problem"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return(redirect('add_tweet'))
        except:
            error="problem"
    return render_template("signup.html")




@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    return render_template("add_tweet.html")


if __name__ == '__main__':
    app.run(debug=True)