import sqlite3

connection  = sqlite3.connect('./flask_rest_with_sqlalchemy/database/my_data.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
# NOTE: To make id column to be autoincrementable in sqlite, we need to mention the data type as 'INTEGER' and PRIMARY KEY.
# If you don't want it to be autoincrementable, then just mention as id int
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)" # real is for decimal
cursor.execute(create_table)

connection.commit()
connection.close()