import sqlite3

conn = sqlite3.connect('database/foodie.db')
cursor = conn.cursor()

# Delete duplicates based on name, keeping the one with the lowest ID
cursor.execute("""
    DELETE FROM menu
    WHERE id NOT IN (
        SELECT MIN(id)
        FROM menu
        GROUP BY name
    )
""")

conn.commit()
conn.close()

print("Duplicates removed.")
