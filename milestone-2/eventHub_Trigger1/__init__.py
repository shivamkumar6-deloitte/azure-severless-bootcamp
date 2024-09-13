

import json
import logging
from datetime import datetime
from azure.functions import EventHubEvent
from typing import List

def parse_and_validate(event):
    try:
        data = json.loads(event.get_body().decode('utf-8'))
        required_fields = ['device_id', 'timestamp', 'aqi', 'temperature', 'humidity', 'co2']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            logging.error("Missing required fields: %s", missing_fields)
            return None

        if not (0 <= data['aqi'] <= 500):
            logging.error("AQI value out of range: %s", data['aqi'])
            return None
        
        return data
    except json.JSONDecodeError as e:
        logging.error("JSON parsing error: %s", e)
        return None

def enrich_data(data):
    data['readable_timestamp'] = datetime.utcfromtimestamp(data['timestamp']).isoformat()
    device_locations = {
        "AQ_sensor_001": "Sector 1",
        "AQ_sensor_002": "landmark 2"
    }
    data['location'] = device_locations.get(data['device_id'], 'Unknown Location')
    
    return data

def main(events: List[EventHubEvent]):
    for event in events:
        data = parse_and_validate(event)
        logging.info('Python EventHub trigger processed an event: %s', data)
        logging.info('enriching the data')
        enriched_data = enrich_data(data)
        logging.info('enriched_data from an event: %s', enriched_data)

