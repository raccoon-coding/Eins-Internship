from flask import request, jsonify, send_file
from flask_restful import Resource
import csv
import os

package_dir = os.getcwd()

# 결과 파일에 대한 API
class OutputsApi(Resource):
    file_path = package_dir+'/result/result.csv'

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