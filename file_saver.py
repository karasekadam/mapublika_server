import os
from flask import request, Blueprint, app

# from app import __name__

file_saver = Blueprint('file_saver', __name__)

UPLOAD_DIRECTORY = "./users_data_sets"
ALLOWED_EXTENSIONS = {'csv'}

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
