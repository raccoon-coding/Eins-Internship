from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, frontend_dir)
from app import server_api_url

bp = Blueprint('detail', __name__, url_prefix='/detail')


# A view controller that shows the input file in table
@bp.route('/<int:file_name>/')
def detail(file_name):
    # user to front server http get request
    # user-specified file name in get request to server
    parameter = {
        "name": file_name
    }
    response = requests.get(server_api_url, params=parameter)
    # return and display data
    datas = response.json()
    return render_template("JsonTable.html", json=datas)