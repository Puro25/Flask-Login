from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from flask.ext.googlemaps import GoogleMaps
import datetime
from flask import session

app = Flask(__name__)
app.secret_key = ':\x00X\xa0\xeeA6\x87\xa0p\\D6F#\xdc\xfc\xb8t\x90\xb6\x9b|\x0e'
client = MongoClient('mongodb://localhost:27017/')
db = client.mytestdb


@app.route('/')
def home():
    return "Hello, World!"  # return a string

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            #return redirect(url_for('home'))
            ip = request.remote_addr
            post = {"ipadd" : ip ,"date": datetime.datetime.utcnow()}
            print ip,datetime.datetime.utcnow()
            post_id = db.data.insert_one(post).inserted_id
            session['logged_in']=True
            return render_template('index.html')
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session['logged_in']= False
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug = True)
