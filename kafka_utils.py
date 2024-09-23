from var import (
    URL_API,
    MAX_LIMIT,
    MAX_OFFSET,
    TOPIC
)

import datetime
import requests
from typing import List
import logging
from kafka import KafkaProducer
import json

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO, force=True)


def create_kafka_producer():
    # Initialize Kafka producer
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9094'],  # Specify your Kafka broker address
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # For serializing JSON messages
    )
    return producer


def kafka_producer(last_processed_timestamp: datetime.datetime) -> List[dict]:
    offset = 0
    full_data_keys = []
    producer = create_kafka_producer()
    while True:
        
        url = URL_API.format(last_processed_timestamp, offset)
        response = requests.get(url)
        data = response.json()
        current_results = data["results"]
        removed_duplicates = [value for value in current_results if value["reference_fiche"] not in full_data_keys]
        full_data_keys.extend(value["reference_fiche"]for value in removed_duplicates)
        offset += len(current_results)
        for message in removed_duplicates: producer.send(TOPIC, value=message) 
        if len(current_results) < MAX_LIMIT:
            break
        # The sum of offset + limit API parameter must be lower than 10000.
        if offset + MAX_LIMIT >= MAX_OFFSET:
            
            last_timestamp = current_results[-1]["date_de_publication"].split("T")[0] 
            timestamp_as_date = datetime.datetime.strptime(last_timestamp, "%Y-%m-%d")
            timestamp_as_date = timestamp_as_date - datetime.timedelta(days=1)
            last_processed_timestamp = timestamp_as_date.strftime("%Y-%m-%d")
            offset = 0

    logging.info(f"Got {len(full_data_keys)} results from the API")