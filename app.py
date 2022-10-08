import pandas as pd
import os
from flask import Flask, render_template, request
from file_saver import UPLOAD_DIRECTORY, allowed_file
import csv_data_processor


app = Flask(__name__)


@app.route('/hello/', methods=['GET', 'POST'])
def welcome_hello():
    return "Hello World!"


@app.route('/')
def welcome():
    return render_template("index.html")


@app.route('/<string:name>/')
def hello(name):
    return "Hello " + name


@app.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""
    if filename not in request.files:
        return "cannot extract file from request", 400
    if "/" in filename:
        return "no subdirectories allowed", 400
    if not allowed_file(filename):
        return "wrong file format, file must be csv", 400
    file_storage = request.files[filename]

    file_storage.save(os.path.join(UPLOAD_DIRECTORY, filename))

    return "", 201


@app.route("/porodnost")
def porodnost():
    return csv_data_processor.to_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    df = pd.read_csv("uzemi_ciselniky.csv")
