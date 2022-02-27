from app import data_handling
from app.models import Tmp, sampleData
import datetime

def check_time_moveless(id_room, day_part):
    print('check time')
    timer_sample = sampleData.query.filter_by(id_room = id_room, 
                                              day_part = day_part).first()
    last_row = Tmp.query.order_by(Tmp.id.desc()).first()

    if last_row is None:
        return

    date = list(map(int, last_row.date.split('/')))
    time = list(map(int, last_row.time.split(':')))

    last_datetime = datetime.datetime(date[2], date[1], date[0], time[0], time[1], time[2])
    real_time = datetime.datetime.now()
    
    diff = int((real_time - last_datetime).total_seconds())
    print(diff)
    if diff >= timer_sample.timer:
        data_handling.collapse(id_room, True, diff)