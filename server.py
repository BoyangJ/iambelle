from flask import Flask, render_template, request

from tweets import get_user_tweets

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/introduceme', methods=['POST'])
def introduce():
    thing = request.form['name']
    thing.replace("@", "")
    # send data to boyangs function
    get_user_tweets(thing)
    return thing
