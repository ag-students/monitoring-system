import json
from flask import request, render_template
from app import app, mqtt_client, db, sample_data
from app.models import Tmp, myData, sampleData, Rooms

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

@app.route('/init_system', methods = ('GET', 'POST'))
def init_system():
    global USER_EMAIL
    if request.method == 'POST':
        mac = request.form.get('mac')
        id_room = request.form.get('id_room')
        email = request.form.get('email')
        if email != "":
            USER_EMAIL = email
            print (USER_EMAIL)
        if (id_room != "" 
            and mac != "" ):
            # room = Rooms.query.filter_by(mac = mac).first()
            # room.id_room = id_room
            # db.session.commit()
            item = json.dumps({'mac': mac, 'id': id_room}, indent = 4)
            mqtt_client.publish('esp/setup', item)
    return render_template('init_id.html')

@app.route('/edit-sample', methods = ('GET', 'POST'))
def edit_sample():
    if request.method == 'POST':
        mac = request.form.get('mac')
        n_time  = request.form.get('night-time')
        n_timer = request.form.get('night-timer')
        m_time  = request.form.get('morning-time')
        m_timer = request.form.get('morning-timer')
        d_time  = request.form.get('day-time')
        d_timer = request.form.get('day-timer')
        e_time  = request.form.get('evening-time')
        e_timer = request.form.get('evening-timer')
        sample_data.edit_sample()
        print (mac, n_time, n_timer)
    return render_template('edit_sample.html')
