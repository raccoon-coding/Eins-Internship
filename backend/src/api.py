from flask import Flask, request, jsonify, send_file
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
import csv
import os

app = Flask(__name__)
api = Api(app)

# Input 파일에 대한 API
class Inputs(Resource):    
    def get(self):
        try:
            format_type = request.args.get('format')
            filename = request.args.get('name')
            file_path = '/home/internship/backend/src/input/'+filename

            if not os.path.exists(file_path):
                return "File not found", 404

            if format_type=='json':
                json_data = self.read_csv_and_convert_to_json(file_path)
                return jsonify(json_data)
            else:
                return send_file(file_path, as_attachment=True)

        except Exception as e:
            return str(e), 500

    def read_csv_and_convert_to_json(self, csv_path):
        json_data = []
        with open(csv_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                json_data.append(row)
        return json_data
    
    
    def post(self):
        try:
            files_list = request.files.getlist("file[]")
            for file in files_list:
                file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input", secure_filename(file.filename))
                file.save(file_path)
            return {'message': 'Input files uploaded successfully.'}
        except Exception as e:
            return str(e), 400

# 결과 파일에 대한 API
class Outputs(Resource):
    def get(self):
        try:
            format_type = request.args.get('format')
            file_path = '/home/internship/backend/result/result.csv'

            if not os.path.exists(file_path):
                return "File not found", 404

            if format_type=='json':
                json_data = self.read_csv_and_convert_to_json(file_path)
                return jsonify(json_data)
            else:
                return send_file(file_path, as_attachment=True)

    def read_csv_and_convert_to_json(self, csv_path):
        json_data = []
        with open(csv_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                json_data.append(row)
        return json_data


api.add_resource(Inputs, '/simulator/inputs')
api.add_resource(Outputs, '/simulator/outputs')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
