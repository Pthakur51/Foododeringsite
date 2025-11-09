import sqlite3

conn = sqlite3.connect('database/foodie.db')  # Adjust the path if needed
cursor = conn.cursor()

cursor.execute("SELECT * FROM menu")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
