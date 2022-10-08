import pandas as pd
import os
from flask import Flask, render_template, request

from csv_parser import read_csv, to_json
from file_saver import UPLOAD_DIRECTORY, allowed_file, save_json, name_file

# import csv_data_processor

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
def post_file(filename: str):
    token = request.headers.get("Authorization").split(" ")[1]

    args = request.form
    print(args.get("value_code"))

    if filename not in request.files:
        return "cannot extract file from request", 400
    if "/" in filename and "__#__" not in filename:
        return "no subdirectories or __#__ allowed", 400
    if not allowed_file(filename):
        return "wrong file format, file must be csv", 400
    file_storage = request.files[filename]

    json_str: str = read_csv(file_storage,
                             args.get("value_code"),
                             args.get("value_occurrences"),
                             args.get("location_text"),
                             args.get("localization_type"))

    new_name = name_file(filename, token)
    save_json(json_str, new_name)

    return "", 201

# @app.route("/files/<filename>", methods=["GET"])
# def filenames_of_user():




# @app.route("/porodnost")
# def porodnost():
#     return csv_data_processor.to_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    df = pd.read_csv("uzemi_ciselniky.csv")
