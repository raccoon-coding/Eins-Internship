from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file
import requests
#
import os
import sys
from frontend.function.ViewFileList import file_list_view

current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, frontend_dir)
from app import server_api_url

bp = Blueprint('delete', __name__, url_prefix='/delete')

# delete Controller
@bp.route('/', methods=['POST', 'GET'])
def delete():
    # if user to front server post request
    if request.method == 'POST':
        # return file name
        scenarios = request.form.getlist('scenarios')
        # http delete request to server
        for scenario in scenarios:
            parameter = {
                "name": scenario
            }
            requests.delete(server_api_url, params=parameter)
        # return file list view
        return file_list_view()
