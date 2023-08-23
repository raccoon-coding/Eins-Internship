from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file
import requests
import io
import os
import sys

from frontend.function.ViewFileList import file_list_view

bp = Blueprint('scenario', __name__, url_prefix='/scenario')
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, frontend_dir)
from app import server_api_url

# A management controller that shows the input file list and connected view
@bp.route('/', methods=['GET', 'POST'])
def scenario_uploads():
    # if user to front server post request
    if request.method == 'POST':
        # Forward the user upload file request to the server as it is
        scenario = request.files.getlist("file[]")
        for file in scenario:
            if file.filename.endswith(".csv"):
                with io.BytesIO() as f:
                    file.save(f)
                    contents = f.getvalue()
                parameter = {
                    "file[]": (file.filename, contents)
                }
                requests.post(server_api_url, files=parameter)
        # display uploaded file list
        return file_list_view()
    else:
        return file_list_view()
