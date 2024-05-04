import sqlite3

def execute(sql, parameters=None):
    connection = sqlite3.connect("league.db")    
    try:
        cursor = connection.cursor()
        if parameters:
            cursor.execute(sql, parameters)
        else:
            cursor.execute(sql) 
        connection.commit()
        rows = cursor.fetchall()
        connection.close()
        return rows
    except sqlite3.Error as e:
        print("Error:", e)
        connection.close()
        raise e