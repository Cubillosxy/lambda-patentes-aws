# tests/test_metrics.py
import json
import sqlite3
import os
import pytest
from lambda_functions.metrics.handler import lambda_handler

# Fixture to set up a temporary SQLite DB for testing
@pytest.fixture(autouse=True)
def setup_db(tmp_path):
    db_file = tmp_path / "db.db"
    # Set environment variable to allow your Lambda code to pick up the test DB path
    os.environ["DB_PATH"] = str(db_file)
    
    # Initialize the test database with schema
    with open("db/schema.sql", "r") as schema:
        conn = sqlite3.connect(str(db_file))
        conn.executescript(schema.read())
        # Optionally, insert test data into readings and exposures
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO readings (reading_id, timestamp, license_plate, checkpoint_id, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
            ("read123", "2025-03-04T10:00:00", "ABC123", "CHECK_01", 40.7128, -74.0060)
        )
        cur.execute(
            "INSERT INTO exposures (reading_id, campaign_id, ad_content, timestamp) VALUES (?, ?, ?, ?)",
            ("read123", "CAMP_001", "AD_001", "2025-03-04T10:00:00")
        )
        conn.commit()
        conn.close()
    yield
    if os.path.exists(str(db_file)):
        os.remove(str(db_file))

def test_metrics_response():
    # Invoke the metrics API
    response = lambda_handler({})
    data = json.loads(response["body"])
    
    # Validate readings per checkpoint
    assert "readings_per_checkpoint" in data
    assert isinstance(data["readings_per_checkpoint"], list)
    
    # Validate ads per campaign
    assert "ads_per_campaign" in data
    assert isinstance(data["ads_per_campaign"], list)
    
    # Validate latest exposures
    assert "latest_exposures" in data
    assert isinstance(data["latest_exposures"], list)
    
    # If the test data was inserted, verify that at least one reading/exposure is present
    assert len(data["readings_per_checkpoint"]) > 0
    assert len(data["ads_per_campaign"]) > 0
    assert len(data["latest_exposures"]) > 0
