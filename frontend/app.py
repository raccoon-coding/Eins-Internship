from flask import Flask

# server url object
server_api_url = 'http://127.0.0.1:8010/simulator/inputs'
return_server_api_url = 'http://127.0.0.1:8010/simulator/outputs'


def create_app():
    app = Flask(__name__)

    # Code to tie together files for each function in Blueprints
    from form.Input import MainView, Reset, Delete, Detail, ScenarioUpload
    app.register_blueprint(MainView.bp)
    app.register_blueprint(Reset.bp)
    app.register_blueprint(Detail.bp)
    app.register_blueprint(Delete.bp)
    app.register_blueprint(ScenarioUpload.bp)

    from form.Output import Result, ResultGraph
    app.register_blueprint(Result.bp)
    app.register_blueprint(ResultGraph.bp)

    return app

# Frontend Sever start function in pont number 8000
if __name__ == '__main__':
    create_app().run(host='0.0.0.0', port=8000)


