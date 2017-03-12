from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/introduceme', methods=['POST'])
def introduce(data):
    # send data to boyangs function
    return ("data")