from flask import Flask, request, jsonify, send_file
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
import csv
import os

app = Flask(__name__)
api = Api(app)
    
# TODO: 일부 파일의 변경이 들어올 때를 고려하기
class UploadFiles(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        try:
            files_list = request.files.getlist("file[]")
            for file in files_list:
                file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "input", secure_filename(file.filename))
                file.save(file_path)
            return {'message': 'Input files uploaded successfully.'}
        except Exception as e:
            return str(e), 400

class DownloadFiles(Resource):
    def get(self):
        try:
            csv_path = '/home/internship/backend/result/result.csv'  # CSV 파일 경로
            json_data = self.read_csv_and_convert_to_json(csv_path)
            return jsonify(json_data)
        except Exception as e:
            return str(e), 500

    def read_csv_and_convert_to_json(self, csv_path):
        json_data = []
        with open(csv_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                json_data.append(row)
        return json_data


api.add_resource(UploadFiles, '/simulator/inputs')
api.add_resource(DownloadFiles, '/simulator/outputs')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
