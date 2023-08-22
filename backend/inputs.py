from flask import request, jsonify, send_file
from flask_restful import Resource
from werkzeug.utils import secure_filename
import csv
import os

package_dir = os.getcwd()

# Input 파일에 대한 API
class InputsApi(Resource):
    dir_path = package_dir + '/input/'

    def get(self):
        try:
            format_type = request.args.get('format')
            filename = request.args.get('name')
            file_list = os.listdir(self.dir_path)
            if filename == 'all' or filename == None:
                if len(file_list) == 0:
                    return jsonify({-1: "None"})

                return file_list

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
            