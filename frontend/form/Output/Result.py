from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, frontend_dir)
from app import return_server_api_url

bp = Blueprint('result', __name__, url_prefix='/result')


# A view controller that shows the result file in table
@bp.route('/', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        # Request result data from server
        parameter = {
            "format": "json"
        }
        response = requests.get(return_server_api_url, params=parameter)
        datas = response.json()
        # display result data
        return render_template("result.html", json=datas)
    elif request.method == 'GET':
        if request.args.get('download') == 'True':
            # Request result file from server
            return file_download()
        else:
            # Request result data from server
            parameter = {
                "format": "json"
            }
            # display result data
            response = requests.get(return_server_api_url, params=parameter)
            datas = response.json()
            return render_template("result.html", json=datas)


def file_download():
    # Download file to user local computer
    # Request to the server in {"format":"csv"} format.
    parameter = {
        "format": "csv"
    }
    response = requests.get(return_server_api_url, params=parameter)
    # Temporary storage for downloading files
    with open('result.csv', 'wb') as file:
        file.write(response.content)
    return send_file('result.csv', as_attachment=True, download_name='result.csv')