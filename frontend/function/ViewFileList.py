from flask import Flask, render_template, request, jsonify, send_file
import requests
#
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, frontend_dir)
from app import server_api_url


def file_list_view():
    # Body in Json{"name":"all}
    parameter = {
        "name": "all"
    }
    # http get request to server
    response = requests.get(server_api_url, params=parameter)
    # return response
    datas = response.json()
    # display uploaded file list
    scenario_list = list()
    for data in datas:
        scenario_list.append(data)
    return render_template("scenario.html", scenario_name=scenario_list)