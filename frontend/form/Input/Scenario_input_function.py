from flask import Blueprint
import os


bp = Blueprint('main', __name__, url_prefix='/')






if __name__ == '__main__':
    app.run(debug=True)
