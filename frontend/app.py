from flask import Flask, render_template, request, jsonify, send_file
from flask_restful import Api
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import io


app = Flask(__name__)
api = Api(app)

server_api_url = 'http://192.168.0.214:8010//simulator/inputs'
return_server_api_url = 'http://192.168.0.214:8010/simulator/outputs'


@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/scenario', methods=['GET', 'POST'])
def scenario_uploads():
    if request.method == 'POST':
        scenario = request.files.getlist("file[]")
        for file in scenario:
            # CSV 파일만 업로드
            if file.filename.endswith(".csv"):
                with io.BytesIO() as f:
                    file.save(f)
                    contents = f.getvalue()
                parameter = {
                    "file[]": {
                        file.name: contents
                    }
                }
                requests.post(server_api_url, files=parameter)
        parameter = {
            "name": "all"
        }
        response = requests.get(server_api_url, params=parameter)
        datas = response.json()
        scenario_list = list()
        for data in datas["files"]:
            scenario_list.append(data)
        return render_template("scenario.html", scenario_name=scenario_list)
    else:
        parameter = {
            "name": "all"
        }
        response = requests.get(server_api_url, params=parameter)
        datas = response.json()
        scenario_list = list()
        for data in datas["file_name"]:
            scenario_list.append(data)
        return render_template("scenario.html", scenario_name=scenario_list)


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        response = requests.get(return_server_api_url)
        csv_data = response.json()
        return render_template("result.html", csv=csv_data)
    elif request.method == 'GET':
        try:
            format_type = request.args.get('format')
            response = requests.get(return_server_api_url)
            datas = response.json()
            if format_type == 'json':
                return render_template("JsonTable.html", json=datas)

        except Exception as e:
            return str(e), 500


@app.route('/result_graph', methods=['POST', 'GET'])
def result_graph():
    if request.method == 'POST':
        response = requests.get(return_server_api_url)
        csv_data = response.json()
        #csv_data = request.files.getlist("file[]")
        dataframes = []
        dataframes.append(csv_data)

        combined_data = pd.concat(dataframes, ignore_index=True)
        combined_data['날짜'] = pd.to_datetime(combined_data['날짜'])

        # Group data by date
        grouped_data = combined_data.groupby(combined_data['날짜'].dt.date)

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


@app.route('/detail/<string:file_name>/')
def link_detail(file_name):
    format_type = request.args.get('format')
    parameter = {
        "name": file_name
    }
    response = requests.get(server_api_url, params=parameter)
    datas = response.json()
    if format_type == 'json':
        return render_template("JsonTable.html", json=datas)
    else:
        return render_template("scenario_list.html", csv=datas)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
