import os
from os import listdir
from os.path import isfile, join

from flask import request, Blueprint, app

# from app import __name__

file_saver = Blueprint('file_saver', __name__)

UPLOAD_DIRECTORY = "./users_data_sets"
ALLOWED_EXTENSIONS = {'csv'}
USER_SEPARATOR = "__#__"
PUB = "pub"
PUB_DATASETS_DIRECTORY = "./public_datasets"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

if not os.path.exists(PUB_DATASETS_DIRECTORY):
    os.makedirs(PUB_DATASETS_DIRECTORY)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_json(json_str: str, filename: str):
    text_file = open(os.path.join(UPLOAD_DIRECTORY, filename), "x")

    text_file.write(json_str)

    text_file.close()


def name_file(filename: str, token: str):
    name = filename.split(".")[0]
    return token + USER_SEPARATOR + name + ".json"


def files_of_user(token: str):
    files = []
    for file in listdir(UPLOAD_DIRECTORY):
        file_split = file.split(USER_SEPARATOR)
        if len(file_split) != 2:
            continue
        prefix = file_split[0]
        if token == prefix:
            files.append(file_split[1].split(".")[0])
    return files


def find_users_file(token, file_name):
    for file in listdir(UPLOAD_DIRECTORY):
        file_split = file.split(USER_SEPARATOR)
        if len(file_split) != 2:
            continue
        prefix = file_split[0]
        if token == prefix:
            file_mid_name = file_split[1].split(".")[0]
            if file_mid_name == file_name:
                with open(os.path.join(UPLOAD_DIRECTORY, file), "r") as f:
                    return f.read()


def public_datasets_service():
    datasets = []
    for ds in listdir(PUB_DATASETS_DIRECTORY):
        ds_split = ds.split(USER_SEPARATOR)
        if len(ds_split) == 2:
            datasets.append(ds_split[1].split(".")[0])
    return datasets


def get_one_public_dataset(name):
    for ds in listdir(PUB_DATASETS_DIRECTORY):
        ds_split = ds.split(USER_SEPARATOR)[1].split(".")[0]
        if name == ds_split:
            with open(os.path.join(PUB_DATASETS_DIRECTORY, ds), "r") as f:
                return f.read()
