# tests/test_process_reading.py
import json
import sqlite3
import os
import pytest
from lambda_functions.process_reading.handler import lambda_handler

# Setup a temporary SQLite DB for tests
@pytest.fixture(autouse=True)
def setup_db(tmp_path):
    db_file = tmp_path / "db.db"
    os.environ["DB_PATH"] = str(db_file)
    with open("db/schema.sql", "r") as schema:
        conn = sqlite3.connect(str(db_file))
        conn.executescript(schema.read())
        conn.commit()
        conn.close()
    yield
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))

def test_valid_reading():
    event = {
        "body": json.dumps({
            "reading_id": "read123",
            "timestamp": "2025-03-04T10:00:00",
            "license_plate": "ABC123",
            "checkpoint_id": "CHECK_01",
            "location": {"latitude": 40.7128, "longitude": -74.0060}
        })
    }
    response = lambda_handler(event)
    data = json.loads(response["body"])
    assert response["statusCode"] == 200
    assert "campaign_applied" in data
