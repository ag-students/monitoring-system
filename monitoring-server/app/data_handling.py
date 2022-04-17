import datetime
from app import gpio, timer, db, mailer
from app.models import Tmp, myData, sampleData

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
    tmp = Tmp(date = content['date'],
              time = content['time'],
              move = content['move'])
    db.session.add(tmp)
    db.session.commit()


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
        if content['id'] == ID_PREV:
            print('No move; ID prev ', ID_PREV, '; ID cur ', content['id'])
            timer.check_time_moveless(content['id'], interval_day)


def verification(time, id_room, day_part):
    print('Verification run')
    global USER_EMAIL
    sample = sampleData.query.filter_by(id_room = id_room, 
                                        day_part = day_part).first()
    # compare with diff
    if time <= sample.time_diff:
        return True
    else:
        mailer.send_mail(USER_EMAIL)
        # gpio.run_pwm()
        return False


# collapse tmp table and run verification
def collapse(id_room, err, timer_time = 0):
    print('Collapse run')
    global USER_EMAIL
    first_row = Tmp.query.first()
    last_row  = Tmp.query.order_by(Tmp.id.desc()).first()

    if first_row is None:
        return

    first_date = list(map(int, first_row.date.split('/')))
    first_time = list(map(int, first_row.time.split(':')))

    last_date = list(map(int, last_row.date.split('/')))
    last_time = list(map(int, last_row.time.split(':')))

    first_date_time = datetime.datetime(first_date[2], first_date[1], first_date[0], first_time[0], first_time[1], first_time[2])
    last_date_time  = datetime.datetime(last_date[2], last_date[1], last_date[0], last_time[0], last_time[1], last_time[2])

    diff = int((last_date_time - first_date_time).total_seconds()) + timer_time
    print("diff = ", diff)
    interval_day = check_interval(first_row.time)
        # delete tmp
    tmp = Tmp.query.all()
    for item in tmp:
        db.session.delete(item)
    db.session.commit()

    if not err:
        print('no error')
        is_abnormal = verification(diff, id_room, interval_day)
        data = myData(id_room     = id_room,
                      date        = first_row.date,
                      time        = diff,
                      day_part    = interval_day,
                      is_abnormal = is_abnormal)
        db.session.add(data)
        db.session.commit()
    else:
        print('error')
        data = myData(id_room     = id_room,
                      date        = first_row.date,
                      time        = diff,
                      day_part    = interval_day,
                      is_abnormal = False)
        db.session.add(data)
        db.session.commit()
        mailer.send_mail(USER_EMAIL)
        # gpio.run_pwm()
        return
