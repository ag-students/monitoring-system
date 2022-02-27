from app import db

class Tmp(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    date        = db.Column(db.String(10), nullable = False)
    time        = db.Column(db.String(10), nullable = False)
    move        = db.Column(db.Boolean, nullable = False)

class myData(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    id_room     = db.Column(db.Integer, nullable = False)
    date        = db.Column(db.String(10), nullable = False)
    time        = db.Column(db.String(10), nullable = False)
    day_part    = db.Column(db.Integer, nullable = False)
    is_abnormal = db.Column(db.Boolean, nullable = False)

class sampleData(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    id_room     = db.Column(db.Integer, nullable = False)
    day_part    = db.Column(db.Integer, nullable = False)
    time_diff   = db.Column(db.Integer, nullable = False)
    timer       = db.Column(db.Integer, nullable = False)

def create_sample_list():
    data1_0 = sampleData(
        id_room     = 1,
        day_part    = 0,
        time_diff   = 60,
        timer       = 60
    )
    data1_1 = sampleData(
        id_room     = 1,
        day_part    = 1,
        time_diff   = 60,
        timer       = 60
    )
    data1_2 = sampleData(
        id_room     = 1,
        day_part    = 2,
        time_diff   = 60,
        timer       = 60
    )
    data1_3 = sampleData(
        id_room     = 1,
        day_part    = 3,
        time_diff   = 60,
        timer       = 60
    )
    data2_0 = sampleData(
        id_room     = 2,
        day_part    = 0,
        time_diff   = 60,
        timer       = 60
    )
    data2_1 = sampleData(
        id_room     = 2,
        day_part    = 1,
        time_diff   = 60,
        timer       = 60
    )
    data2_2 = sampleData(
        id_room     = 2,
        day_part    = 2,
        time_diff   = 60,
        timer       = 60
    )
    data2_3 = sampleData(
        id_room     = 2,
        day_part    = 3,
        time_diff   = 60,
        timer       = 60
    )

    sample_list = [data1_0, data1_1, data1_2, data1_3,
                   data2_0, data2_1, data2_2, data2_3]
    return sample_list
