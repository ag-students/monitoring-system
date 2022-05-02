import ydb
import os

# Необходимое для подключения
endpoint = 'grpcs://ydb.serverless.yandexcloud.net:2135'
database = '/ru-central1/b1gv4ndsnlo51urgt1ae/etnfn3c07b3a6qgpgi6u'
# Команда для получения токена: yc iam create-token
YDB_ACCESS_TOKEN_CREDENTIALS = "t1.9euelZqNlYudjMyNj8rLkJmekZiXmu3rnpWajJjPlI_ImprOysyUzY6ZmYzl9PcnN0Bs-e86ZmDI3fT3Z2U9bPnvOmZgyA.gGj03Sa3A7ZqIAlwvC6zZGrYKMx1Z2FPJbRsVzWqqA3LW16EbpUcwVi-wsyor4pVX48X97IgC5nCxBgc6PR5CA"
path = "" # Этот путь нужен, если наши таблицы лежат не в корневой директории

# Подключение и работа с БД
def run(endpoint, database, path):
    # Создание драйвера (отвечает за транспортный уровень)
    # Подключаемся через токен

    stream = os.popen('yc iam create-token')
    token = stream.read().strip()
    print (token)
    driver_config = ydb.DriverConfig(
        endpoint, database, credentials=ydb.AccessTokenCredentials(token)
    )
    with ydb.Driver(driver_config) as driver:
        try:
            driver.wait(fail_fast=True, timeout=5)
            # Создание сессии
            session = driver.table_client.session().create()
            upsert_simple(session, database)
        except TimeoutError:
            print("Connect failed to YDB")
            print("Last reported errors by discovery:")
            print(driver.discovery_debug_details())
            exit(1)

# Добавление данных
def upsert_simple(session, path):
    session.transaction().execute(
        """
        PRAGMA TablePathPrefix("{}");
        UPSERT INTO Users (id, address, e_mail, name, surname) VALUES
            ({}, "{}", "{}", "{}", "{}");
        """.format(path, 2, '12dsvsdvz', "test@test.com", 'fpewkqnegf', 'TBD'),
        commit_tx=True,
    )

# Точка входа
if __name__ == "__main__":
    run(endpoint, database, path)
