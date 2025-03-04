CREATE TABLE IF NOT EXISTS readings (
    reading_id TEXT PRIMARY KEY,
    timestamp TEXT,
    license_plate TEXT,
    checkpoint_id TEXT,
    latitude REAL,
    longitude REAL
);

CREATE TABLE IF NOT EXISTS exposures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reading_id TEXT,
    campaign_id TEXT,
    ad_content TEXT,
    timestamp TEXT
);