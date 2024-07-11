import sqlite3

conn = sqlite3.connect('url_shortener.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM url_mapping')
rows = cursor.fetchall()

for row in rows:
    print(f"Short URL: {row[0]} - Original URL: {row[1]}")  # Assuming short_url is the first column, original_url is the second

conn.close()
