from app import db

class Users(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(20), nullable = False)
    surname     = db.Column(db.String(30), nullable = False)
    e_mail      = db.Column(db.String(30), nullable = False)
    address     = db.Column(db.String(30), nullable = False)
    rooms       = db.relationship('Rooms', backref = 'user', lazy = 'dynamic')

class Rooms(db.Model):
    id_room     = db.Column(db.Integer, primary_key = True)
    mac         = db.Column(db.String(20), nullable = False)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'))
    data        = db.relationship('myData', backref = 'rooms', lazy = 'dynamic')
    sample      = db.relationship('sampleData', backref = 'rooms', lazy = 'dynamic')

class myData(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    id_room     = db.Column(db.Integer, db.ForeignKey('rooms.id_room'))
    date        = db.Column(db.String(10), nullable = False)
    time        = db.Column(db.String(10), nullable = False)
    day_part    = db.Column(db.Integer, nullable = False)
    is_abnormal = db.Column(db.Boolean, nullable = False)

class sampleData(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    id_room     = db.Column(db.Integer, db.ForeignKey('rooms.id_room'))
    day_part    = db.Column(db.Integer, nullable = False)
    time_diff   = db.Column(db.Integer, nullable = False)
    timer       = db.Column(db.Integer, nullable = False)

class Tmp(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    date        = db.Column(db.String(10), nullable = False)
    time        = db.Column(db.String(10), nullable = False)
    move        = db.Column(db.Boolean, nullable = False)
