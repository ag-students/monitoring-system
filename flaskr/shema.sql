-- Init db

DROP TABLE IF EXISTS tmp_1;
DROP TABLE IF EXISTS myData;
DROP TABLE IF EXISTS sampleData;

CREATE TABLE tmp_1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_ TEXT NOT NULL,
    time_ TEXT NOT NULL,
    move_ BOOLEAN NOT NULL
);

CREATE TABLE myData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_room INTEGER NOT NULL,
    date_ TEXT NOT NULL,
    time_ TEXT NOT NULL,
    interval_day INTEGER NOT NULL,
    is_abnormal BOOLEAN NOT NULL
);

CREATE TABLE sampleData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_room INTEGER NOT NULL,
    interval_day INTEGER NOT NULL,
    time_diff INTEGER NOT NULL, -- in seconds
    timer INTEGER NOT NULL    -- in seconds
);

INSERT INTO sampleData 
    (id_room, interval_day, time_diff, timer) 
VALUES 
    (1, 0, 60, 60),
    (1, 1, 60, 60),
    (1, 2, 60, 60),
    (1, 3, 60, 60),
    (2, 0, 60, 60),
    (2, 1, 60, 60),
    (2, 2, 60, 60),
    (2, 3, 60, 60);