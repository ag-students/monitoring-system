import json
from flask import request, render_template
from app import app, mqtt_client
from app.models import Tmp, myData, sampleData

@app.route('/')
def home():
    lists = myData.query.all()
    return render_template('data.html', lists = lists)

@app.route('/tmp')
def tmp():
    lists = Tmp.query.all()
    return render_template('tmp.html', lists = lists)

@app.route('/sample')
def sample():
    lists = sampleData.query.all()
    return render_template('sample.html', lists = lists)

@app.route('/init_id', methods = ('GET', 'POST'))
def init_id():
    if request.method == 'POST':
        mac = request.form.get('mac')
        id_room = request.form.get('id_room')
        item = json.dumps({'mac': mac, 'id': id_room}, indent = 4)
        mqtt_client.publish('esp/setup', item)
    return render_template('init_id.html')

