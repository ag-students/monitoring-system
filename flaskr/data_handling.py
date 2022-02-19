from .db import get_db
import datetime
from . import gpio
from . import timer

global ID_PREV
ID_PREV = 0

# intervals of days:
def check_interval(time):
    hour = list(map(int, time.split(':')))
    # 00:00 - 06:00 -- night [0]
    if 0 <= hour[0] < 6:
        return 0

    # 06:00 - 12:00 -- morning [1]
    if 6 <= hour[0] < 12:
        return 1

    # 12:00 - 18:00 -- day [2]
    if 12 <= hour[0] < 18:
        return 2        

    # 18:00 - 00:00 -- evening [3]
    if 18 <= hour[0] < 24:
        return 3

def insert_into_tmp(content):
    db = get_db()
    db.execute(
        "INSERT INTO tmp_1 (date_, time_, move_) VALUES (?, ?, ?)",
        (content['date'], content['time'], content['move'])
    )
    db.commit()

def handler(content, interval_day):
    global ID_PREV

    if content['move'] == 1:
        if content['id'] == ID_PREV:
            print('Move; ID prev ', ID_PREV, '; ID cur ', content['id'])
            timer.check_time_moveless(content['id'], interval_day)
            insert_into_tmp(content)
        else:
            print('Move; ID prev ', ID_PREV, '; ID cur ', content['id'])
            collapse(ID_PREV, False)
            ID_PREV = content['id']
            insert_into_tmp(content)
    else:
        print('No move; ID prev ', ID_PREV, '; ID cur ', content['id'])
        timer.check_time_moveless(content['id'], interval_day)

    # if content['id'] == 1:
    #     if content['move'] == 1:
    #         if ID_PREV == 1:
    #             ID_PREV = 1
    #             print('1_1_1')
    #             timer.check_time_moveless(content['id'], interval_day)
    #             insert_into_tmp(content)
    #         else:
    #             print('1_1_2')
    #             collapse(ID_PREV, False)
    #             ID_PREV = content['id']
    #             insert_into_tmp(content)                    
    #     elif ID_PREV == 1:
    #         print('1_2')
    #         timer.check_time_moveless(content['id'], interval_day)
    # elif content['id'] == 2:
    #     if content['move'] == 1:
    #         if ID_PREV == 2:
    #             ID_PREV = 2
    #             print('2_1_1')
    #             timer.check_time_moveless(content['id'], interval_day)
    #             insert_into_tmp(content)
    #         else:
    #             print('2_1_2')
    #             collapse(ID_PREV, False)
    #             ID_PREV = content['id']
    #             insert_into_tmp(content)                    
    #     elif ID_PREV == 2:
    #         print('2_2')
    #         timer.check_time_moveless(content['id'], interval_day)


def verification(time, id_room, interval_day):
    print('Verification run')
    db = get_db()
    sample = db.execute(
        "SELECT time_diff FROM sampleData WHERE id_room = ? AND interval_day = ?",
        (id_room, interval_day)
    ).fetchone()
    # compare with diff
    if time <= sample['time_diff']:
        return True
    else:
        gpio.run_pwm()
        return False


# collapse tmp table and run verification
def collapse(id_room, err, timer_time = 0):
    print('Collapse run')
    db = get_db()
    first_row = db.execute(
        "SELECT * FROM tmp_1 ORDER BY id LIMIT 1"
    ).fetchone()
    last_row = db.execute(
        "SELECT * FROM tmp_1 ORDER BY id DESC LIMIT 1"
    ).fetchone()

    if first_row is None:
        return

    first_date = list(map(int, first_row['date_'].split('/')))
    first_time = list(map(int, first_row['time_'].split(':')))

    last_date = list(map(int, last_row['date_'].split('/')))
    last_time = list(map(int, last_row['time_'].split(':')))

    first_date_time = datetime.datetime(first_date[2], first_date[1], first_date[0], first_time[0], first_time[1], first_time[2])
    last_date_time = datetime.datetime(last_date[2], last_date[1], last_date[0], last_time[0], last_time[1], last_time[2])

    diff = int((last_date_time - first_date_time).total_seconds()) + timer_time
    print("diff = ", diff)
    interval_day = check_interval(first_row['time_'])
        # delete tmp
    db.execute(
        "DELETE FROM tmp_1"
    )
    db.commit()

    if not err:
        print('no error')
        is_abnormal = verification(diff, id_room, interval_day)
        db.execute(
            "INSERT INTO myData (id_room, date_, time_, interval_day, is_abnormal) VALUES (?, ?, ?, ?, ?)",
            (id_room, first_row['date_'], diff, interval_day, is_abnormal)
        )
        db.commit()
    else:
        print('error')
        db.execute(
            "INSERT INTO myData (id_room, date_, time_, interval_day, is_abnormal) VALUES (?, ?, ?, ?, ?)",
            (id_room, first_row['date_'], diff, interval_day, False)
        )
        db.commit()
        gpio.run_pwm()
        return
