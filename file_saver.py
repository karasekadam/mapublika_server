import os
from flask import request, api

UPLOAD_DIRECTORY = "/./users_data_sets"

if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)


@api.route("/files/<filename>", methods=["POST"])
def post_file(filename):
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        os.abort(400, "no subdirectories allowed")

    with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201
