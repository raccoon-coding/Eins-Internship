from flask import request, jsonify, send_file
from flask_restful import Resource
from werkzeug.utils import secure_filename
import csv
import os

package_dir = os.getcwd()

# Input 파일에 대한 API
class InputsApi(Resource):

    #input 경로
    dir_path = package_dir + '/input/'

    #GET method
    def get(self):
        try:
            #파라미터 확인
            format_type = request.args.get('format', 'json', str)
            filename = request.args.get('name', 'all', str)

            #파일 목록 불러오기
            file_list = os.listdir(self.dir_path)
            if filename == 'all' or filename == None:
                if len(file_list) == 0:
                    return jsonify({-1: "None"})

                return file_list

            #파일 내용 불러오기
            file_path = self.dir_path + file_list[int(filename)]
            if not os.path.exists(file_path):
                return "File not found", 404

            if format_type == 'csv':
                return send_file(file_path, as_attachment=True)
            else:
                json_data = self.read_csv_and_convert_to_json(file_path)
                return json_data
        
        #GET method 실패 응답
        except Exception as e:
            return str(e), 500
    
    def delete(self):
        try:
            filename = request.args.get('name', 'all', str)

            if filename=='all':
                self.delete_all_files(self.dir_path)
            else:     
                file_path = self.dir_path + secure_filename(filename)
                if os.path.exists(file_path):
                    try:                      
                        os.remove(file_path)
                        return {'message': f'File {filename} deleted successfully.'}
                    except Exception as e:
                        return {'message': f'Failed to delete file {filename}. Reason: {str(e)}'}, 500
                else:
                    return {'message': f'File {filename} not found.'}, 404

        #DELETE method 실패 응답
        except Exception as e:
            return str(e), 500
            
    # input 파일 삭제 함수
    def delete_all_files(self,directory_path):
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    self.delete_all_files(file_path)
                    os.rmdir(file_path)
            
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")

    # csv to json 변환 함수
    def read_csv_and_convert_to_json(self, csv_path):
        data = []
        with open(csv_path, 'r', encoding='utf-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                data.append(row)
            print(data)
        return jsonify(data)

    #POST method 
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
            