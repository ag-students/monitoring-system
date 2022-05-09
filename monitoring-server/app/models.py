from app import db

class Users(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(20), nullable = False)
    surname     = db.Column(db.String(30), nullable = False)
    e_mail      = db.Column(db.String(30), nullable = False)
    address     = db.Column(db.String(30), nullable = False)
    rooms       = db.relationship('Rooms', backref = 'user', lazy = 'dynamic', cascade = 'all, delete')

    def __repr__(self):
        return 'User: {} {} {} {} {}'.format(self.id, 
                                             self.name, 
                                             self.surname, 
                                             self.address, 
                                             self.e_mail)

class Rooms(db.Model):
    id_room     = db.Column(db.Integer, primary_key = True)
    mac         = db.Column(db.String(20), nullable = False)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"))
    data        = db.relationship('myData', backref = 'rooms', lazy = 'dynamic', cascade = 'all, delete')
    sample      = db.relationship('sampleData', backref = 'rooms', lazy = 'dynamic', cascade = 'all, delete')

    def __repr__(self):
        return 'Room: {} {} {}'.format(self.id_room, self.mac, self.user_id)

class myData(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    id_room     = db.Column(db.Integer, db.ForeignKey('rooms.id_room', onupdate="CASCADE", ondelete="CASCADE"))
    date        = db.Column(db.String(10), nullable = False)
    time        = db.Column(db.String(10), nullable = False)
    day_part    = db.Column(db.Integer, nullable = False)
    is_abnormal = db.Column(db.Boolean, nullable = False)

    def __repr__(self):
        return 'myData: {} {} {} {} {} {}'.format(self.id, 
                                                  self.id_room, 
                                                  self.date, 
                                                  self.time, 
                                                  self.day_part, 
                                                  self.is_abnormal)

class sampleData(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    id_room     = db.Column(db.Integer, db.ForeignKey('rooms.id_room', onupdate="CASCADE", ondelete="CASCADE"))
    day_part    = db.Column(db.Integer, nullable = False)
    time_diff   = db.Column(db.Integer, nullable = False)
    timer       = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return 'Sample: {} {} {} {} {}'.format(self.id, 
                                               self.id_room,
                                               self.day_part, 
                                               self.time_diff,
                                               self.timer)

class Tmp(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    date        = db.Column(db.String(10), nullable = False)
    time        = db.Column(db.String(10), nullable = False)
    move        = db.Column(db.Boolean, nullable = False)
