# Flight Tracker Producer

![Python 3.9](https://img.shields.io/badge/Python-3.9-blue)
![Pytest 8.3.5](https://img.shields.io/badge/Pytest-8.3.5-blue)
![Quixstreams 3.12.0](https://img.shields.io/badge/Quixstreams-3.12.0-orange)
![Kafka 4](https://img.shields.io/badge/Kafka-4-red)


A Python application that fetches real-time flight data from the OpenSky Network and publishes it to Kafka.

## Features

- Fetches real-time flight data from OpenSky Network
- Configurable geographic boundaries for flight tracking
- Publishes flight data to Kafka topics
- Configurable via environment variables or command-line arguments
- Docker support with crontab scheduling

## Prerequisites

- Python 3.8 or higher
- Kafka broker (local or remote)
- OpenSky Network API access
- Docker (optional, for containerized deployment)

## Installation

### Local Installation

1. Clone the repository:
```bash
git clone git@github.com:luismr/flight-tracker-event-producer-python.git
cd flight-tracker-event-producer-python
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure it:
```bash
cp .env.example .env
```

### Docker Installation

1. Build the Docker image:
```bash
docker build -t flight-tracker-producer .
```

2. Run the container:
```bash
docker run -d \
  --name flight-tracker \
  -e CRON_SCHEDULE="*/5 * * * *" \
  -e KAFKA_BOOTSTRAP_SERVERS="broker1:9092,broker2:9092,broker3:9092" \
  -e KAFKA_TOPIC=flight-positions \
  -e LAT_MIN=-33.75 \
  -e LAT_MAX=5.27 \
  -e LON_MIN=-73.99 \
  -e LON_MAX=-34.79 \
  flight-tracker-producer
```

3. View logs:
```bash
docker logs -f flight-tracker
```

4. Stop the container:
```bash
docker stop flight-tracker
docker rm flight-tracker
```

## Kafka

Apache Kafka is a distributed event streaming platform that we use to publish and subscribe to flight data events. It provides high-throughput, fault-tolerant handling of real-time data feeds.

### Running Kafka Locally

For development and testing purposes, you can run a single Kafka broker locally:

1. Start a Kafka broker using Docker with proper advertised listeners configuration:
```bash
docker run -d \
  -p 9092:9092 \
  --name broker \
  -e KAFKA_BROKER_ID=1 \
  -e KAFKA_LISTENERS=PLAINTEXT://:9092 \
  -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 \
  -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 \
  apache/kafka:latest
```

2. Wait a few seconds for the broker to start up.

3. To stop the broker:
```bash
docker stop broker
docker rm broker
```

Note: The `KAFKA_ADVERTISED_LISTENERS` should match your Docker environment:
- For local development: `PLAINTEXT://localhost:9092`
- For Docker network: `PLAINTEXT://broker:9092`
- For external access: `PLAINTEXT://your-external-ip:9092`

### Running Kafka Cluster

For production environments, we recommend using a Kafka cluster for better reliability and scalability. You can use the [kafka-cluster-docker-compose](https://github.com/luismr/kafka-cluster-docker-compose) repository which provides a complete setup for a 3-broker Kafka cluster using KRaft mode (ZooKeeper-free).

The cluster setup includes:
- 3 Kafka brokers configured as both brokers and controllers
- Plaintext communication between brokers
- Automatic topic replication
- Kafdrop UI for cluster management (accessible on port 19000)

To use the cluster setup:

1. Clone the repository:
```bash
git clone git@github.com:luismr/kafka-cluster-docker-compose.git
cd kafka-cluster-docker-compose
```

2. Create the required network:
```bash
docker network create kafka-net
```

3. Configure the cluster ID in `.env` file:
```bash
cp .env.example .env
# Edit .env and set KAFKA_CLUSTER_ID=your-unique-cluster-id
```

4. Start the cluster:
```bash
docker-compose up -d
```

The cluster will be accessible on ports 19092, 19093, and 19094. Update your application's `KAFKA_BOOTSTRAP_SERVERS` environment variable to:
```
localhost:19092,localhost:19093,localhost:19094
```

For more details about the cluster setup, including configuration options and management tools, refer to the [kafka-cluster-docker-compose](https://github.com/luismr/kafka-cluster-docker-compose) repository.

## Configuration

The application can be configured using environment variables or command-line arguments:

### Environment Variables

- `OPENSKY_URL`: OpenSky Network API URL (default: https://opensky-network.org/api/states/all)
- `KAFKA_BOOTSTRAP_SERVERS`: Kafka broker addresses (default: localhost:9092). For clusters, provide a comma-separated list of broker:port pairs, e.g., "broker1:9092,broker2:9092,broker3:9092"
- `KAFKA_TOPIC`: Kafka topic for flight data (default: flight-positions)
- `LAT_MIN`: Minimum latitude for flight tracking (default: -33.75)
- `LAT_MAX`: Maximum latitude for flight tracking (default: 5.27)
- `LON_MIN`: Minimum longitude for flight tracking (default: -73.99)
- `LON_MAX`: Maximum longitude for flight tracking (default: -34.79)
- `CRON_SCHEDULE`: Crontab expression for scheduling (default: "*/5 * * * *")

### Command-line Arguments

- `--kafka`: Send data to Kafka instead of printing to stdout (default: False)

## Usage

### Print to stdout (Default)

```bash
python main.py
```

This will fetch flight data and print it to stdout in JSON format.

### Publish to Kafka

```bash
python main.py --kafka
```

This will fetch flight data and publish it to the configured Kafka topic.

## Project Structure

```
flight-tracker-producer/
├── main.py                 # Main application entry point
├── opensky/                # OpenSky Network API client
│   └── opensky_client.py
├── events/                 # Event handling and Kafka producer
│   └── event_producer.py
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
├── .env                    # Environment variables (create from .env.example)
├── Dockerfile              # Container configuration
└── README.md               # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Testing

The project includes a comprehensive test suite using pytest. To run the tests:

1. Install the package with test dependencies:
```bash
pip install -e ".[test]"
```

2. Run the tests:
```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=.

# Run specific test file
pytest tests/test_opensky_client.py
```

The test suite includes:
- Unit tests for OpenSkyClient
- Unit tests for EventProducer
- Unit tests for main application
- Mocked external dependencies (OpenSky API, Kafka)
- Coverage reporting 
## License

This project is licensed under the MIT License - see the LICENSE file for details.

