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
  "databaseURL": "https://meettutorial-cda45-default-rtdb.europe-west1.firebasedatabase.app/"
};


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'




@app.route('/', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method == "POST":
        login_session['email'] = request.form['email']
        login_session['password'] = request.form['password']
        try:
            login_session['user'] = user = auth.sign_in_with_email_and_password(login_session["email"], login_session["password"])
            return(redirect('add_tweet'))
        except:
            error="problem"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == "POST":
        login_session['email']= request.form['email']
        login_session['password'] = request.form['password']
        login_session['full_name']= request.form['full_name']
        login_session['bio'] = request.form['bio']
        login_session['username']= request.form['username']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(login_session["email"], login_session["password"])
            user= {"email": request.form['email'],"password": request.form['password'],"full_name": request.form['full_name'],"username": request.form['username'],"bio": request.form['bio'],}
            user = db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect('add_tweet')
        except:
            return render_template("signup.html", error="problem")
    else:
        return render_template("signup.html")


@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == "POST":
        login_session['title'] = request.form['title']
        login_session['text'] = request.form['text']
        tweet = {"title": login_session['title'],"text": login_session['text'],"uid":login_session['user']['localId'], "username": login_session['username'] }
        try:
            tweet = db.child("Tweets").push(tweet)
        except:
            return render_template("add_tweet.html", error="problem")
    return render_template("add_tweet.html")

#app.route('/all_tweets', methods=['GET', 'POST'])
#def all_tweets():
    #return render_template("tweets.html", tweets=db.child("Tweets").get().val())


@app.route('/all_tweets', methods=['GET', 'POST'])
def all_tweets():
    return render_template('tweets.html', tweets =db.child("Tweets").get().val())


if __name__ == '__main__':
    app.run(debug=True)