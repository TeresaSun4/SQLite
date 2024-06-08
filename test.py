import sqlite3

db = sqlite3.connect('cd.dp.db')
cursor = db.cursor
sql = "SELECT * FROM sign_up;"

db.close()