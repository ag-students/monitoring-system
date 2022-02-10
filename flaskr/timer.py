from .db import get_db
from . import data_processing
import datetime

def check_time_moveless(id_room, interval_day):
    print('check time')
    db = get_db()
    timer_sample = db.execute(
        "SELECT timer FROM sampleData WHERE id_room=? AND interval_day=?",
        (id_room, interval_day)
    ).fetchone()

    last_row = db.execute(
        "SELECT * FROM tmp_1 ORDER BY id DESC LIMIT 1"
    ).fetchone()

    if last_row is None:
        return

    date = list(map(int, last_row['date_'].split('/')))
    time = list(map(int, last_row['time_'].split(':')))

    last_datetime = datetime.datetime(date[2], date[1], date[0], time[0], time[1], time[2])
    real_time = datetime.datetime.now()
    
    diff = int((real_time - last_datetime).total_seconds())
    print(diff)
    if diff >= timer_sample['timer']:
        data_processing.collapse(id_room, True, diff)