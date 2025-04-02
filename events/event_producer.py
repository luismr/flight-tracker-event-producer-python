import json
import logging

from quixstreams import Application


class EventProducer:
    """
    EventProducer is a class that produces events to a Kafka topic.
    """

    def __init__(self, config: dict):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.logger.debug("EventProducer initialized with config: %s", self.config)

    def submit_event(self, flight_data: list):
        app = Application(
            broker_address=self.config['KAFKA_BOOTSTRAP_SERVERS'],
            loglevel=self.config['KAFKA_LOGLEVEL']
        )
        self.logger.debug("Application initialized with config: %s", self.config)
        with app.get_producer() as producer:
            for data in flight_data:
                self.logger.debug("Producing event to Kafka Topic '%s': (%s) %s", self.config['KAFKA_TOPIC'], data['icao24'], data)
                producer.produce(
                    topic=self.config['KAFKA_TOPIC'],
                    key=data['icao24'],
                    value=json.dumps(data)
                )
