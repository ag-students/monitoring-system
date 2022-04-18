import json
from flask import redirect, request, render_template, url_for
from app import app, mqtt_client, db, sample_data
from app.models import Tmp, myData, sampleData, Rooms, Users

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

@app.route('/rooms')
def rooms():
    lists = Rooms.query.all()
    return render_template('rooms.html', lists = lists)

@app.route('/init_system', methods = ('GET', 'POST'))
def init_system():
    global USER_EMAIL
    user = Users.query.get(1)
    if request.method == 'POST':
        name = request.form.get('name')
        surname = request.form.get('surname')
        address = request.form.get('address')
        email = request.form.get('email')
        USER_EMAIL = email
        print (USER_EMAIL)
        u = Users.query.get(1)
        if u is None:
            u_new = Users(name = name, 
                          surname = surname, 
                          e_mail = email, 
                          address = address)
            db.session.add(u_new)
            db.session.commit()
            return render_template('init_system.html', lists = user)
        u.name = name
        u.surname = surname
        u.e_mail = email
        u.address = address
        db.session.commit()  
    return render_template('init_system.html', lists = user)

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
        sample_data.edit_sample(mac, n_time, n_timer, 
                                m_time, m_timer, 
                                d_time, d_timer,
                                e_time, e_timer)
    return render_template('edit_sample.html')

@app.route('/edit-rooms', methods = ('GET', 'POST'))
def edit_rooms():
    if request.method == 'POST':
        mac = request.form.get('mac')
        id_room = request.form.get('id_room')
        if Rooms.query.filter_by(mac = mac).first() is None:
            r = Rooms(id_room = id_room, mac = mac, user_id = 1)
            db.session.add(r)
            db.session.commit()
            return redirect(url_for('rooms'))
        room = Rooms.query.filter_by(mac = mac).first()
        room.id_room = id_room
        db.session.commit()
        item = json.dumps({'mac': mac, 'id': id_room}, indent = 4)
        mqtt_client.publish('esp/setup', item)
    return render_template('edit_room.html')

@app.route('/start_system')
def start_system():
    rooms = Rooms.query.all()
    for item in rooms:
        str = json.dumps({'mac': item.mac, 'id': item.id_room}, indent = 4)
        mqtt_client.publish('esp/setup', str)
    return redirect(url_for('home'))

@app.route('/stop_system')
def stop_system():
    rooms = Rooms.query.all()
    for item in rooms:
        str = json.dumps({'mac': item.mac, 'id': 0}, indent = 4)
        mqtt_client.publish('esp/setup', str)
    # collapse table and finish current data analyze 
    return redirect(url_for('home'))
