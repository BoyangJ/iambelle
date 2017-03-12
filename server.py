from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/introduceme', methods=['POST'])
def introduce():
    thing = request.form['name']
    # send data to boyangs function
    return thing