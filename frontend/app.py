import csv
import json
from plotly.subplots import make_subplots
from flask import Flask, render_template, request, jsonify, send_file
from flask_restful import Api
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import io


app = Flask(__name__)
api = Api(app)

# server url object
server_api_url = 'http://127.0.0.1:5000/simulator/inputs'
return_server_api_url = 'http://127.0.0.1:5000/simulator/outputs'


# Main view controller
@app.route('/')
def upload_file():
    parameter = {
        "name": "all"
    }
    requests.delete(server_api_url, params=parameter)
    return render_template('scenario.html')


# A management controller that shows the input file list and connected view
@app.route('/scenario', methods=['GET', 'POST'])
def scenario_uploads():
    if request.method == 'POST':
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
        
        parameter = {"name": "all"}
        response = requests.get(server_api_url, params=parameter)
        datas = response.json()
        scenario_list = list()
        for data in datas:
            scenario_list.append(data)
        return render_template("scenario.html", scenario_name=scenario_list)
    else:
        parameter = {
            "name": "all"
        }
        response = requests.get(server_api_url, params=parameter)
        datas = response.json()
        scenario_list = list()
        for data in datas:
            scenario_list.append(data)
        return render_template("scenario.html", scenario_name=scenario_list)


# delete Controller
@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        scenarios = request.form.getlist('scenarios')
        for scenario in scenarios:
            parameter = {
                "name": scenario
            }
            requests.delete(server_api_url, params=parameter)
        parameter = {
            "name": "all"
        }
        response = requests.get(server_api_url, params=parameter)
        datas = response.json()
        scenario_list = list()
        for data in datas:
            scenario_list.append(data)
        return render_template("scenario.html", scenario_name=scenario_list)


# Reset Controller
@app.route('/reset', methods=['POST', 'GET'])
def reset():
    if request.method == 'POST':
        parameter = {
            "name": "all"
        }
        requests.delete(server_api_url, params=parameter)
        parameter = {
            "name": "all"
        }
        response = requests.get(server_api_url, params=parameter)
        datas = response.json()
        if datas['-1'] == 'None':
            return render_template("scenario.html")
        scenario_list = list()
        for data in datas:
            scenario_list.append(data)
        return render_template("scenario.html", scenario_name=scenario_list)


# A view controller that shows the result file in table
@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        parameter = {
            "format": "json"
        }
        response = requests.get(return_server_api_url, params=parameter)
        datas = response.json()
        return render_template("result.html", json=datas)
    elif request.method == 'GET':
        parameter = {
            "format": "csv"
        }
        requests.get(return_server_api_url, params=parameter)
        parameter = {
            "format": "json"
        }
        response = requests.get(return_server_api_url, params=parameter)
        datas = response.json()
        return render_template("result.html", json=datas)


# A view controller that shows the result file in graph
@app.route('/result_graph', methods=['POST', 'GET'])
def result_graph():
    if request.method == 'POST':
        parameter = {
            "format": "json"
        }
        response = requests.get(return_server_api_url, params=parameter)
        json_data = response.json()

        output = io.StringIO()
        writer = csv.writer(output)

        header = json_data[0].keys() if json_data else []
        writer.writerow(header)

        for row in json_data:
            writer.writerow(row.values())

        csv_output = output.getvalue()
        output.seek(0)
        dataframe = pd.read_csv(output)
        output.close()

        dataframe['날짜'] = pd.to_datetime(dataframe['날짜'])

        grouped_data = dataframe.groupby(dataframe['날짜'].dt.date)

        fig = go.Figure()
        color_scale = px.colors.qualitative.Set1  # You can use any color palette

        for i, (date, group) in enumerate(grouped_data):
            color_idx = i % len(color_scale)
            color = color_scale[color_idx]

            fig.add_trace(go.Scatter(x=group['측정 시작 시각'], y=group['통과차량'], mode='lines',
                                     name=str(date), line=dict(color=color)))

        fig.update_layout(title='CSV Data Graph', xaxis_title='측정 시작 시각', yaxis_title='통과차량')
        graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')  # Use Plotly.js from CDN

        return render_template("ResultGraph.html", graph_html=graph_html)


# A view controller that shows the input file in table
@app.route('/detail/<string:file_name>/')
def detail(file_name):
    format_type = request.args.get('format')
    parameter = {
        "name": file_name
    }
    response = requests.get(server_api_url, params=parameter)
    datas = response.json()
    return render_template("JsonTable.html", json=datas)


# Frontend Sever start function in pont number 8000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
