from flask import Flask
from flask_restful import Api
from inputs import InputsApi
from result import OutputsApi

app = Flask(__name__)
api = Api(app)

api.add_resource(InputsApi, '/simulator/inputs')
api.add_resource(OutputsApi, '/simulator/outputs')

if __name__ == '__main__':
    #API 서버 포트 OPEN : 5000
    app.run(host='0.0.0.0', port=8010)