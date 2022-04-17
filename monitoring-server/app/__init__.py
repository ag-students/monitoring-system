import os
import json
import paho.mqtt.client as mqtt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

global USER_EMAIL
USER_EMAIL = ''

PROJECT_ROOT        = os.path.abspath(os.path.dirname(__file__))
MQTT_BROKER_URL     = "localhost"
MQTT_BROKER_PORT    = 1883
MQTT_CLIENT_ID      = 'flask_mqtt'
MQTT_CLEAN_SESSION  = True
MQTT_USERNAME       = 'ololo534'
MQTT_PASSWORD       = '5073'
MQTT_KEEPALIVE      = 60

SETUP_ESP = ["""
{
    "mac": "BC:FF:4D:35:A1:6E",
    "id": 1
}
""",
"""
{
    "mac": "BC:FF:4D:35:46:22",
    "id": 2
}
"""]

app = Flask(__name__)

app.config.from_mapping(
    HOST = "0.0.0.0",
    SECRET_KEY = '89bdd76801421bcfa9fc6e147f1d68f40a0bd248a70ed8429d9c1dc3',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'app.db'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for item in SETUP_ESP:
        client.publish('esp/setup', item)
    client.subscribe('ololo/pir_data')

def on_message(client, userdata, message):
    print('Received message on topic {}: {}'
          .format(message.topic, message.payload.decode()))
    content = json.loads(message.payload.decode())
    interval_day = data_handling.check_interval(content['time'])
    print (content, interval_day)
    data_handling.handler(content, interval_day)


mqtt_client = mqtt.Client(client_id = MQTT_CLIENT_ID,
                          clean_session = MQTT_CLEAN_SESSION)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.username_pw_set(username = MQTT_USERNAME,
                            password = MQTT_PASSWORD)
mqtt_client.connect(MQTT_BROKER_URL,
                    MQTT_BROKER_PORT,
                    MQTT_KEEPALIVE)
mqtt_client.loop_start()

from app import routes, models, data_handling
