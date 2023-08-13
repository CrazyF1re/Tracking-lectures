import sqlite3

async def set_data(arr):
    database = sqlite3.connect("lectures.db")
    sql = database.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS lectures (
        url TEXT,
        time BIGINT,
        UNIQUE(url)
        )""")
    database.commit()
    for i in arr:
        sql.execute("""INSERT OR IGNORE into lectures VALUES(?,?)""",(i[0],i[1]))
        database.commit()
    sql.close()
    database.close()

async def get_last_record():
    database = database = sqlite3.connect("lectures.db")
    sql = database.cursor()
    return sql.execute("""SELECT FROM lectures WHERE TIME = (SELECT MAX(TIME) from lectures)""").fetchone()
    