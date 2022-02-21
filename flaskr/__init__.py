import os
import json
from flask import Flask, request, render_template
from flask_mqtt import Mqtt
from .db import get_db
from . import data_handling

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))


def create_app():
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY          = 'dev',
        MQTT_BROKER_URL     = 'localhost',
        MQTT_BROKER_PORT    = 1883,
        MQTT_CLIENT_ID      = 'flask_mqtt',
        MQTT_CLEAN_SESSION  = True,
        MQTT_USERNAME       = 'ololo534',
        MQTT_PASSWORD       = '5073',
        MQTT_KEEPALIVE      = 5,
        MQTT_TLS_ENABLED    = False,
        DATABASE = os.path.join(PROJECT_ROOT, 'flaskr.sqlite')
    )
    mqtt = Mqtt()

    with app.app_context():
        from . import db
        db.init_app(app)
        mqtt.init_app(app)

    @mqtt.on_connect()
    def handle_connect(client, userdata, flags, rc):
        mqtt.publish('esp/setup', '{\n  "mac": "BC:FF:4D:35:A1:6E",\n  "id": 1\n}')
        mqtt.subscribe('ololo/pir_data')
    
    @mqtt.on_message()
    def handle_mqtt_message(client, userdata, message):
        print('Received message on topic {}: {}'
              .format(message.topic, message.payload.decode()))
        content = json.loads(message.payload.decode())
        interval_day = data_handling.check_interval(content['time'])
        print (content, interval_day)

        data_handling.handler(content, interval_day)
        
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


    return app
