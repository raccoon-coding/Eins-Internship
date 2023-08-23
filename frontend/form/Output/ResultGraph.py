import csv
from flask import Blueprint
from flask import Flask, render_template, request, jsonify, send_file
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import io
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(current_dir, '..', '..', '..')
sys.path.insert(0, frontend_dir)
from app import return_server_api_url

bp = Blueprint('result_graph', __name__, url_prefix='/result_graph')


# A view controller that shows the result file in graph
@bp.route('/', methods=['POST', 'GET'])
def result_graph():
    if request.method == 'POST':
        # Request result data from server
        parameter = {
            "format": "json"
        }
        response = requests.get(return_server_api_url, params=parameter)
        json_data = response.json()
        # json to csv format
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
        # grouping '날짜'
        dataframe['날짜'] = pd.to_datetime(dataframe['날짜'])

        grouped_data = dataframe.groupby(dataframe['날짜'].dt.date)

        fig = go.Figure()
        color_scale = px.colors.qualitative.Set1  # You can use any color palette
        # Color by group
        for i, (date, group) in enumerate(grouped_data):
            color_idx = i % len(color_scale)
            color = color_scale[color_idx]

            fig.add_trace(go.Scatter(x=group['측정 시작 시각'], y=group['통과차량'], mode='lines',
                                     name=str(date), line=dict(color=color)))
        # return graph
        fig.update_layout(title='CSV Data Graph', xaxis_title='측정 시작 시각', yaxis_title='통과차량')
        graph_html = fig.to_html(full_html=False, include_plotlyjs='cdn')  # Use Plotly.js from CDN
        # display view
        return render_template("ResultGraph.html", graph_html=graph_html)