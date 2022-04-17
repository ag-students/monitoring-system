import click
from app import app, db, sample_data
from app.models import Tmp, myData, sampleData

@app.cli.group()
def database():
    pass

@database.command()
def init_sample_data():
    list = sample_data.create_sample_list()
    db.session.add_all(list)
    db.session.commit()
    click.echo('sample data init')

@database.command()
def clear_db():
    tmp = Tmp.query.all()
    for item in tmp:
        db.session.delete(item)
    my_data = myData.query.all()
    for item in my_data:
        db.session.delete(item)
    db.session.commit()
    click.echo('tables Tmp & myData is clear')

@database.command()
def clear_sample_data():
    sample_data = sampleData.query.all()
    for item in sample_data:
        db.session.delete(item)
    db.session.commit()
    click.echo('sample data is clear')
