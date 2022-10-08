import pandas as pd
import os
from flask import Flask, render_template, request
from flask_cors import CORS

import csv_data_processor
from csv_parser import read_csv, to_json
from file_saver import UPLOAD_DIRECTORY, allowed_file, save_json, name_file, \
    files_of_user, find_users_file, public_datasets_service

# import csv_data_processor

app = Flask(__name__)
CORS(app)



@app.route('/hello/', methods=['GET', 'POST'])
def welcome_hello():
    return "Hello World!"


@app.route('/')
def welcome():
    return render_template("index.html")


# @app.route('/<string:name>/')
# def hello(name):
#     return "Hello " + name


@app.route("/files/<filename>/", methods=["POST"])
def post_file(filename: str):
    token = request.headers.get("Authorization").split(" ")[1]

    args = request.form
    print(args.get("value_code"))

    if "/" in filename or "__#__" in filename:
        return "no subdirectories or __#__ allowed", 400
    if not allowed_file(filename):
        return "wrong file format, file must be csv", 400
    file_storage = request.files["file"]

    json_str: str = str(read_csv(file_storage,
                             args.get("value_code"),
                             args.get("value_occurrences"),
                             args.get("location_text"),
                             args.get("localization_type"),
                             average=args.get("average")))


    new_name = name_file(filename, token)
    save_json(json_str, new_name)

    return "", 201


@app.route("/user-datasets/", methods=["GET"])
def filenames_of_user():
    token = request.headers.get("Authorization").split(" ")[1]
    return files_of_user(token)


@app.route("/dataset/<file_name>/", methods=["GET"])
def specific_datasets(file_name):
    token = request.headers.get("Authorization").split(" ")[1]
    result = find_users_file(token, file_name)
    if result is None:
        return 404
    return result


@app.route("/dataset/public/", methods=["GET"])
def public_datasets():
    return public_datasets_service()


@app.route("/porodnost/")
def porodnost():
    return csv_data_processor.to_json()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    df = pd.read_csv("uzemi_ciselniky.csv")
    filenames_of_user()
