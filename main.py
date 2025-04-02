import os
import argparse
import logging

from dotenv import load_dotenv

from opensky.opensky_client import OpenSkyClient
from events.event_producer import EventProducer

# Default configuration

DEFAULT_CONFIG = {
    'OPENSKY_URL': 'https://opensky-network.org/api/states/all',
    'KAFKA_BOOTSTRAP_SERVERS': 'localhost:9092',
    'KAFKA_TOPIC': 'flight-positions',
    'KAFKA_LOGLEVEL': 'INFO',
    'LOGLEVEL': 'INFO',
    'LAT_MIN': -33.75,
    'LAT_MAX': 5.27,
    'LON_MIN': -73.99,
    'LON_MAX': -34.79
}

def get_config():
    """Get configuration from environment variables or command line arguments."""
    config = DEFAULT_CONFIG.copy()
    
    # Update with environment variables if they exist
    for key in config:
        env_value = os.getenv(key)
        if env_value is not None:
            if key in ['LAT_MIN', 'LAT_MAX', 'LON_MIN', 'LON_MAX']:
                config[key] = float(env_value)
            else:
                config[key] = env_value
    
    logging.basicConfig(
        level=config['LOGLEVEL'],
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )

    return config

def run_once(config, print_mode=False):
    """Run the flight tracker once with the given configuration.
    Args:
        config (dict): The configuration dictionary.
        print_mode (bool): Whether to print the data to stdout.
    """
    client = OpenSkyClient(config['OPENSKY_URL'])
    flight_data = client.process_flight_data(config['LAT_MIN'], config['LAT_MAX'], config['LON_MIN'], config['LON_MAX'], print_mode)

    if flight_data:
        producer = EventProducer(config)
        producer.submit_event(flight_data)

def main():
    # Load environment variables
    load_dotenv()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Flight Tracker Event Producer')
    parser.add_argument('--kafka', action='store_true',
                      help='Send data to Kafka instead of printing to stdout')
    args = parser.parse_args()
    
    config = get_config()
    
    logging.debug("Flight Tracker Event Producer started")
    
    run_once(config, print_mode=not args.kafka)  # Print by default unless --kafka is specified

    logging.debug("Flight Tracker Event Producer finished")


if __name__ == '__main__':
    main() 