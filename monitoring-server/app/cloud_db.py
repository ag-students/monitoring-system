import ydb
import os
from dotenv import load_dotenv
from app.models import myData, sampleData, Users, Rooms

load_dotenv()

endpoint = os.getenv('YDB_ENDPOINT')
database = os.getenv('YDB_DATABASE')
path = ""

def run():
    stream = os.popen('yc iam create-token')
    token = stream.read().strip()
    driver_config = ydb.DriverConfig(
        endpoint, database, credentials = ydb.AccessTokenCredentials(token)
    )
    driver = ydb.Driver(driver_config)
    try:
        driver.wait(fail_fast=True, timeout=10)
        session = driver.table_client.session().create()
        return(session)
    except TimeoutError:
        print("Connect failed to YDB")
        print("Last reported errors by discovery:")
        print(driver.discovery_debug_details())
        exit(1)

def upsert_user(session, path = database):
    user = Users.query.get(1)
    session.transaction().execute(
        """
        PRAGMA TablePathPrefix("{}");
        UPSERT INTO Users (id, address, e_mail, name, surname) VALUES
            ({}, "{}", "{}", "{}", "{}");
        """.format(path, 1, user.address, user.e_mail, user.name, user.surname),
        commit_tx=True,
    )


def upsert_rooms(session, path = database):
    rooms = Rooms.query.all()
    for item in rooms:
        session.transaction().execute(
            """
            PRAGMA TablePathPrefix("{}");
            DELETE FROM Rooms WHERE mac == "{}";
            """.format(path, item.mac),
            commit_tx=True,
        )
    for item in rooms:
        session.transaction().execute(
            """
            PRAGMA TablePathPrefix("{}");
            UPSERT INTO Rooms (id_room, mac, user_id) VALUES
                ({}, "{}", {});
            """.format(path, item.id_room, item.mac, item.user_id),
            commit_tx=True,
        )

def upsert_sample(session, path = database):
    samples = sampleData.query.all()
    for item in samples:
        session.transaction().execute(
            """
            PRAGMA TablePathPrefix("{}");
            UPSERT INTO sampleData (id, day_part, id_room, time_diff, timer) VALUES
                ({}, {}, {}, {}, {});
            """.format(path, item.id, item.day_part, item.id_room, item.time_diff, item.timer),
            commit_tx=True,
        )
