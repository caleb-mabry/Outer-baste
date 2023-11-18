CREATE TABLE temperature_data (
    id INTEGER PRIMARY KEY,
    temperature REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);