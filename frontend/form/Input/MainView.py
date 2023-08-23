from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file
import requests
import os
import sys


bp = Blueprint('main', __name__, url_prefix='/')
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, frontend_dir)
from app import server_api_url

# Main view controller
@bp.route('/')
def upload_file():
    # reset uploaded file list and display main view
    parameter = {
        "name": "all"
    }
    requests.delete(server_api_url, params=parameter)
    return render_template('scenario.html')