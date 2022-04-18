from app import db
from app.models import sampleData, Rooms

def create_sample(id_room, n_time, n_timer, m_time, m_timer, d_time, d_timer, e_time, e_timer):
    data1_0 = sampleData(
        id_room     = id_room,
        day_part    = 0,
        time_diff   = n_time,
        timer       = n_timer
    )
    data1_1 = sampleData(
        id_room     = id_room,
        day_part    = 1,
        time_diff   = m_time,
        timer       = m_timer
    )
    data1_2 = sampleData(
        id_room     = id_room,
        day_part    = 2,
        time_diff   = d_time,
        timer       = d_timer
    )
    data1_3 = sampleData(
        id_room     = id_room,
        day_part    = 3,
        time_diff   = e_time,
        timer       = e_timer
    )

    sample_list = [data1_0, data1_1, data1_2, data1_3]
    db.session.add_all(sample_list)
    db.session.commit()
    return

def edit_sample(mac, n_time, n_timer, m_time, m_timer, d_time, d_timer, e_time, e_timer):
    room = Rooms.query.filter_by(mac = mac).first()

    if room.sample.all() == []:
        create_sample(room.id_room, n_time, n_timer, m_time, m_timer, d_time, d_timer, e_time, e_timer)
        return
    
    sample_n = room.sample.filter_by(day_part = 0).first()
    sample_n.time_diff  = n_time
    sample_n.timer      = n_timer

    sample_m = room.sample.filter_by(day_part = 1).first()
    sample_m.time_diff  = m_time
    sample_m.timer      = m_timer

    sample_d = room.sample.filter_by(day_part = 2).first()
    sample_d.time_diff  = d_time
    sample_d.timer      = d_timer

    sample_e = room.sample.filter_by(day_part = 3).first()
    sample_e.time_diff  = e_time
    sample_e.timer      = e_timer
    db.session.commit()
    return