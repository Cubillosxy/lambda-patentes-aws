import json
from datetime import datetime, time
import sqlite3

CAMPAIGN_RULE = {
    "campaign_id": "CAMP_001",
    "locations": ["CHECK_01", "CHECK_02"],
    "time_window": {
        "start": "08:00",
        "end": "20:00"
    },
    "max_exposures_per_plate": 3,
    "ad_content": "AD_001"
}


def within_time_window(timestamp_str, start_str, end_str):
    ts = datetime.fromisoformat(timestamp_str)
    start_time = datetime.strptime(start_str, "%H:%M").time()
    end_time = datetime.strptime(end_str, "%H:%M").time()
    return start_time <= ts.time() <= end_time

def count_exposures(license_plate, conn):
    sql_query = "SELECT COUNT(*) FROM exposures WHERE reading_id IN (SELECT reading_id FROM readings WHERE license_plate=?)"
    cur = conn.cursor()
    cur.execute(sql_query, (license_plate,))
    count = cur.fetchone()[0]
    return count


def lambda_handler(event, context=None):

    try:
        data = json.loads(event.get("body", "{}"))
        reading_id = data["reading_id"]
        timestamp = data["timestamp"]
        license_plate = data["license_plate"]
        checkpoint_id = data["checkpoint_id"]
        location = data["location"]
        latitude = location["latitude"]
        longitude = location["longitude"]
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid input format", "details": str(e)})
        }
    
    conn = sqlite3.connect("db.db")
    
    cur = conn.cursor()
    cur.execute(
        "INSERT OR IGNORE INTO readings (reading_id, timestamp, license_plate, checkpoint_id, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?)",
        (reading_id, timestamp, license_plate, checkpoint_id, latitude, longitude)
    )
    
    apply_campaign = False
    if checkpoint_id in CAMPAIGN_RULE["locations"] and within_time_window(timestamp, CAMPAIGN_RULE["time_window"]["start"], CAMPAIGN_RULE["time_window"]["end"]):
        exposures_count = count_exposures(license_plate, conn)
        if exposures_count < CAMPAIGN_RULE["max_exposures_per_plate"]:
            apply_campaign = True

    if apply_campaign:
        cur.execute(
            "INSERT INTO exposures (reading_id, campaign_id, ad_content, timestamp) VALUES (?, ?, ?, ?)",
            (reading_id, CAMPAIGN_RULE["campaign_id"], CAMPAIGN_RULE["ad_content"], timestamp)
        )
    
    conn.commit()
    conn.close()
    
    response_body = {
        "reading_id": reading_id,
        "campaign_applied": apply_campaign,
        "ad_content": CAMPAIGN_RULE["ad_content"] if apply_campaign else None
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }