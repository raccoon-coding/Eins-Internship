from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
import sys
from frontend.function.ViewFileList import file_list_view

current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, frontend_dir)
from app import server_api_url

bp = Blueprint('reset', __name__, url_prefix='/reset')


# Reset Controller
@bp.route('/', methods=['POST', 'GET'])
def reset():
    # user to front post request
    if request.method == 'POST':
        # reset uploaded file list
        parameter = {
            "name": "all"
        }
        requests.delete(server_api_url, params=parameter)
        # display uploaded file list
        parameter = {
            "name": "all"
        }
        response = requests.get(server_api_url, params=parameter)
        datas = response.json()
        # If the response is {"-1":"None"} then successfully reset
        if datas['-1'] == 'None':
            return render_template("scenario.html")
        else:
            return file_list_view()
