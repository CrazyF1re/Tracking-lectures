import sqlite3



async def set_data(arr):
    database = sqlite3.connect("lectures.db")
    sql = database.cursor()
    sql.execute("""CREATE TABLE IF NOT EXISTS lectures (
        url TEXT,
        time TEXT,
        UNIQUE(url)
        )""")
    database.commit()
    for i in arr:
        sql.execute("""INSERT OR IGNORE into lectures VALUES(?,?)""",(i[0],i[1]))
        database.commit()
    sql.close()
    database.close()
    