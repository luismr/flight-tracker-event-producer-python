import pytest
from unittest.mock import Mock, patch
import json
from datetime import datetime

@pytest.fixture
def mock_response():
    """Mock response from OpenSky API"""
    mock = Mock()
    mock.json.return_value = {
        'states': [
            [
                'abc123',  # icao24
                'TEST123',  # callsign
                'Brazil',  # origin_country
                None,  # time_position
                None,  # time_velocity
                -45.0,  # longitude
                -23.0,  # latitude
                10000.0,  # altitude
                False,  # on_ground
                200.0,  # velocity
                180.0,  # true_track
                0.0,  # vertical_rate
                None,  # sensors
                10000.0,  # geo_altitude
                '1234',  # squawk
                False,  # spi
                0  # position_source
            ]
        ]
    }
    return mock

@pytest.fixture
def mock_kafka_producer():
    """Mock Kafka producer"""
    with patch('quixstreams.Application') as mock_app:
        mock_producer = Mock()
        mock_app.return_value.get_producer.return_value.__enter__.return_value = mock_producer
        yield mock_producer

@pytest.fixture
def sample_config():
    """Sample configuration for testing"""
    return {
        'KAFKA_BOOTSTRAP_SERVERS': 'localhost:9092',
        'KAFKA_TOPIC': 'test-topic',
        'KAFKA_LOGLEVEL': 'INFO'
    }

@pytest.fixture
def sample_flight_data():
    """Sample flight data for testing"""
    timestamp = datetime.now().isoformat()
    return [{
        'timestamp': timestamp,
        'icao24': 'abc123',
        'callsign': 'TEST123',
        'origin_country': 'Brazil',
        'longitude': -45.0,
        'latitude': -23.0,
        'altitude': 10000.0,
        'on_ground': False,
        'velocity': 200.0,
        'true_track': 180.0,
        'vertical_rate': 0.0,
        'geo_altitude': 10000.0,
        'squawk': '1234'
    }] 