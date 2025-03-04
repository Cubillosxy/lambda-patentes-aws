import json
import sqlite3

def lambda_handler(event, context=None):
    conn = sqlite3.connect("db.db")
    cur = conn.cursor()
    
    # Total readings per checkpoint
    cur.execute("SELECT checkpoint_id, COUNT(*) as total_readings FROM readings GROUP BY checkpoint_id")
    readings_per_checkpoint = [{"checkpoint_id": row[0], "total_readings": row[1]} for row in cur.fetchall()]
    
    # Total advertisements shown per campaign
    cur.execute("SELECT campaign_id, COUNT(*) as total_ads FROM exposures GROUP BY campaign_id")
    ads_per_campaign = [{"campaign_id": row[0], "total_ads": row[1]} for row in cur.fetchall()]
    
    # List of latest exposures (last 10)
    cur.execute("SELECT reading_id, campaign_id, ad_content, timestamp FROM exposures ORDER BY timestamp DESC LIMIT 10")
    latest_exposures = [
        {"reading_id": row[0], "campaign_id": row[1], "ad_content": row[2], "timestamp": row[3]} 
        for row in cur.fetchall()
    ]
    
    conn.close()
    
    response_body = {
        "readings_per_checkpoint": readings_per_checkpoint,
        "ads_per_campaign": ads_per_campaign,
        "latest_exposures": latest_exposures
    }
    
    return {
        "statusCode": 200,
        "body": json.dumps(response_body)
    }
