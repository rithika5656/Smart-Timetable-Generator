import sqlite3
import os

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'scheduler.db')
    schema_path = os.path.join(base_dir, 'schema.sql')
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
        
    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == '__main__':
    init_db()
