import sqlite3

connect = sqlite3.connect("Database.db")
cursor = connect.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Scores (
        ID       INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_user  INTEGER REFERENCES Users (ID),
        time     TEXT,
        tour     INTEGER,
        rank     TEXT,
        task_1   INTEGER,
        task_2   INTEGER,
        task_3   INTEGER,
        task_4   INTEGER,
        task_5   INTEGER,
        task_6   INTEGER,
        task_7   INTEGER,
        task_8   INTEGER   
    );
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        ID          INTEGER PRIMARY KEY AUTOINCREMENT,
        name        TEXT,
        surname     TEXT,
        patronymic  TEXT,
        form        INTEGER,
        region      TEXT,
        school      TEXT
    );
""")
connect.commit()
connect.close()
