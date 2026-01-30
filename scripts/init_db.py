import sqlite3
import os

def init_db():
    db_path = 'scheduler.db'
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    
    with open('schema.sql', 'r') as f:
        conn.executescript(f.read())
        
    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == '__main__':
    init_db()
