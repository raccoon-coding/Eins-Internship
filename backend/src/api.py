from flask import Flask, request, jsonify, send_file
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename
import csv
import os

app = Flask(__name__)
api = Api(app)


# Input 파일에 대한 API
class Inputs(Resource):
    dir_path = '/home/temp/Eins-Internship/backend/src/input/'

    def get(self):
        try:
            format_type = request.args.get('format')
            filename = request.args.get('name')
            file_list = os.listdir(self.dir_path)
            if filename == 'all' or filename == None:
                if len(file_list) == 0:
                    return jsonify({-1: "None"})

                return file_list
                # return jsonify({key:value for key, value in enumerate(file_list)})

            file_path = self.dir_path + file_list[int(filename)]
            if not os.path.exists(file_path):
                return "File not found", 404

            if format_type == 'csv':
                return send_file(file_path, as_attachment=True)
            else:
                json_data = self.read_csv_and_convert_to_json(file_path)
                return json_data
        except Exception as e:
            return str(e), 500

    def read_csv_and_convert_to_json(self, csv_path):
        data = []
        with open(csv_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
            print(data)
        return jsonify(data)

    def post(self):
        try:
            list = request.files.getlist("file[]")
            for file in list:
                file_path = self.dir_path + secure_filename(file.filename)
                file.save(file_path)
                print('num_of_files : ' + str(len(os.listdir(self.dir_path))))
            return {'num_of_files': str(len(os.listdir(self.dir_path)))}
        except Exception as e:
            return str(e), 400


# 결과 파일에 대한 API
class Outputs(Resource):
    file_path = '/home/temp/Eins-Internship/backend/result/result.csv'

    def get(self):
        try:
            format_type = request.args.get('format')
            file_path = self.file_path
            if not os.path.exists(file_path):
                return "File not found", 404

            if format_type == 'csv':
                return send_file(file_path, as_attachment=True)
            else:
                json_data = self.read_csv_and_convert_to_json(file_path)
                return json_data
        except Exception as e:
            return str(e), 500

    def read_csv_and_convert_to_json(self, csv_path):
        data = []
        with open(csv_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
        return jsonify(data)


api.add_resource(Inputs, '/simulator/inputs')
api.add_resource(Outputs, '/simulator/outputs')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)