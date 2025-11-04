# app/app.py
from flask import Flask
import os
import pymysql

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "db")
DB_USER = os.environ.get("DB_USER", "user")
DB_PASS = os.environ.get("DB_PASS", "password")
DB_NAME = os.environ.get("DB_NAME", "appdb")
DB_PORT = int(os.environ.get("DB_PORT", 3306))

def get_conn():
    return pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASS,
                           database=DB_NAME, port=DB_PORT, cursorclass=pymysql.cursors.DictCursor)

@app.route("/")
def index():
    conn = get_conn()
    with conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS visits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                count INT NOT NULL
            );
        """)
        # ensure single row exists
        cur.execute("SELECT count FROM visits WHERE id = 1;")
        row = cur.fetchone()
        if row:
            new = row['count'] + 1
            cur.execute("UPDATE visits SET count=%s WHERE id=1;", (new,))
        else:
            new = 1
            cur.execute("INSERT INTO visits (count) VALUES (%s);", (new,))
        conn.commit()
    return f"Hello — DB visits: {new}\n"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
