import json
from quixstreams import Application


class EventProducer:
    """
    EventProducer is a class that produces events to a Kafka topic.
    """

    def __init__(self, config: dict):
        self.config = config


    def submit_event(self, flight_data: list):
        app = Application(
            broker_address=self.config['KAFKA_BOOTSTRAP_SERVERS'],
            loglevel=self.config['KAFKA_LOGLEVEL']
        )

        with app.get_producer() as producer:
            for data in flight_data:
                producer.produce(
                    topic=self.config['KAFKA_TOPIC'],
                    key=data['icao24'],
                    value=json.dumps(data)
                )
