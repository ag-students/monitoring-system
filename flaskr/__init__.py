import os
from flask import Flask, request, render_template
from .db import get_db
from . import data_processing
from . import timer


global ID_PREV
ID_PREV = 1

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))

def insert_into_tmp(content):
    db = get_db()
    db.execute(
        "INSERT INTO tmp_1 (date_, time_, move_) VALUES (?, ?, ?)",
        (content['date'], content['time'], content['move'])
    )
    db.commit()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(PROJECT_ROOT, 'flaskr.sqlite')
    )

    @app.route('/post_json', methods = ['POST'])
    def post_json_handler():
        # global var
        global ID_PREV
        
        # get json and calc interval of day 
        content = request.get_json()
        interval_day = data_processing.check_interval(content['time'])
        print (content, interval_day)

        if content['id'] == 1:
            if content['move'] == 1:
                if ID_PREV == 1:
                    ID_PREV = 1
                    print('1_1_1')
                    timer.check_time_moveless(content['id'], interval_day)
                    insert_into_tmp(content)
                else:
                    print('1_1_2')
                    data_processing.collapse(ID_PREV, False)
                    ID_PREV = content['id']
                    insert_into_tmp(content)                    
            elif ID_PREV == 1:
                print('1_2')
                timer.check_time_moveless(content['id'], interval_day)

        elif content['id'] == 2:
            if content['move'] == 1:
                if ID_PREV == 2:
                    ID_PREV = 2
                    print('2_1_1')
                    timer.check_time_moveless(content['id'], interval_day)
                    insert_into_tmp(content)
                else:
                    print('2_1_2')
                    data_processing.collapse(ID_PREV, False)
                    ID_PREV = content['id']
                    insert_into_tmp(content)                    
            elif ID_PREV == 2:
                print('2_2')
                timer.check_time_moveless(content['id'], interval_day)
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
