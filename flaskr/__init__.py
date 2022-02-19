import os
from flask import Flask, request, render_template
from .db import get_db
from . import data_handling

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


def create_app():
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(PROJECT_ROOT, 'flaskr.sqlite')
    )

    @app.route('/post_json', methods = ['POST'])
    def post_json_handler():
        # get json and calc interval of day 
        content = request.get_json()
        interval_day = data_handling.check_interval(content['time'])
        print (content, interval_day)

        data_handling.handler(content, interval_day)
        return 'JSON posted'

    @app.route('/tmp')
    def tmp():
        db = get_db()
        lists = db.execute(
            "SELECT * FROM tmp_1"
        ).fetchall()
        return render_template('tmp.html', lists = lists)

    @app.route('/')
    def home():
        db = get_db()
        lists = db.execute(
            "SELECT * FROM myData"
        ).fetchall()
        return render_template('data.html', lists = lists)

    from . import db
    db.init_app(app)

    return app
