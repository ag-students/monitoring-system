import click
from app import app, db, sample_data, cloud_db
from app.models import Tmp, myData, sampleData, Users, Rooms

@app.cli.group()
def database():
    pass

@database.command()
def init_sample_data():
    sample_data.create_sample(1, 60, 60, 60, 60, 60, 60, 60, 60)
    sample_data.create_sample(2, 60, 60, 60, 60, 60, 60, 60, 60)
    click.echo('sample data init')

@database.command()
def clear_db():
    tmp = Tmp.query.all()
    for item in tmp:
        db.session.delete(item)
    my_data = myData.query.all()
    for item in my_data:
        db.session.delete(item)
    rooms = Rooms.query.all()
    for item in rooms:
        db.session.delete(item)
    db.session.commit()
    click.echo('tables Tmp, myData & Rooms is clear')

@database.command()
def clear_sample_data():
    sample_data = sampleData.query.all()
    for item in sample_data:
        db.session.delete(item)
    db.session.commit()
    click.echo('sample data is clear')

@database.command()
def clear_user_data():
    users = Users.query.all()
    for item in users:
        db.session.delete(item)
    db.session.commit()
    click.echo('users is clear')

@database.command()
def recreate_rooms():
    rooms = Rooms.query.all()
    for item in rooms:
        db.session.delete(item)
    db.session.commit()
    r1 = Rooms(id_room = 1, mac = "BC:FF:4D:35:A1:6E", user_id = 1)
    r2 = Rooms(id_room = 2, mac = "BC:FF:4D:35:46:22", user_id = 1)
    db.session.add(r1)
    db.session.add(r2)
    db.session.commit()
    click.echo('Rooms is clear')

@app.cli.group()
def cloud():
    pass

@cloud.command()
def test():
    session = cloud_db.run()
    cloud_db.upsert_user(session)

@cloud.command()
def init_rooms():
    session = cloud_db.run()
    cloud_db.upsert_rooms(session)
    
@cloud.command()
def init_sample():
    session = cloud_db.run()
    cloud_db.upsert_sample(session)
