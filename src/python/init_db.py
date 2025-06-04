import sqlite3

SQL_FILE = r"E:\Lab_6_BD\src\sql\lab6.sql"
DB_FILE = r"E:\Lab_6_BD\src\sql\lab6.db"

def initialize_database():
    with open(SQL_FILE, 'r', encoding='utf-8') as f:
        sql_script = f.read()

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.executescript(sql_script)
    conn.commit()
    conn.close()
    print("✅ База даних успішно створена та ініціалізована!")

if __name__ == "__main__":
    initialize_database()
