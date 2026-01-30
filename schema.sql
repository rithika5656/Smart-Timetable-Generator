-- History table to track generation stats
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    subjects TEXT NOT NULL,
    teachers TEXT NOT NULL,
    periods INTEGER NOT NULL,
    duration REAL,
    status TEXT
);
