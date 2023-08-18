from flask import Flask, render_template, request, jsonify, send_file
import os
from flask_restful import Api, Resource
import csv
from werkzeug.utils import secure_filename
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


app = Flask(__name__)
api = Api(app)
file_name_list = list()
number = 0


@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/scenario', methods=['GET', 'POST'])
def scenario_uploads():
    global number
    if request.method == 'POST':
        scenario = request.files.getlist("file[]")
        if number == 0:
            for i in scenario:
                filename = os.getcwd() + "/save csv/" + secure_filename(i.filename)
                i.save(filename)
                number = number + 1
                file_name_list.append(i.filename)
        return render_template("scenario.html", number=number, scenario_name=file_name_list)
    else:
        if number != 0:
            return render_template("scenario.html", number=number, scenario_name=file_name_list)
        else:
            return "you didn't send the file"


# @app.route('/result', methods=['POST', 'GET'])
# def result():
#     if request.method == 'POST':
#         directory_path = os.getcwd() + "/result"
#         for filename in os.listdir(directory_path):
#             if filename.endswith(".csv"):
#                 file_path = os.path.join(directory_path, filename)
#                 with open(file_path, 'rt') as f:
#                     csv_reader = csv.reader(f, delimiter=',')
#                     #csv_data = list(csv_reader)
#     csv_reader = pd.read_csv(file_path)
#     fig = px.line(csv_reader, x='측정 시작 시각', y='통과차량', title='CSV Data Graph')
#     return fig.write_html('ResultGraph.html')
#     #return render_template("ResultGraph.html", csv=csv_data)

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        directory_path = os.getcwd() + "/result"
        dataframes = []

        for filename in os.listdir(directory_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory_path, filename)
                csv_data = pd.read_csv(file_path)
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


@app.route('/detail/<int:file_name_number>/')
def detail(file_name_number):
    filename = os.getcwd() + "/save csv/"
    filename = filename + file_name_list[file_name_number]
    with open(filename, 'rt') as f:
        csvd = csv.reader(f, delimiter=',')
        csv_data = list(csvd)  # Read the entire CSV data into a list
        return render_template("scenario_list.html", csv=csv_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
