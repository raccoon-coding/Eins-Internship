from flask import Flask, render_template, request, jsonify, send_file
import os
from flask_restful import Api, Resource
import csv
from werkzeug.utils import secure_filename

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


@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        directory_path = os.getcwd() + "/result"
        for filename in os.listdir(directory_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'rt') as f:
                    csv_reader = csv.reader(f, delimiter=',')
                    csv_data = list(csv_reader)
    return render_template("result.html", csv=csv_data)


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
