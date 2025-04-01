import pytest
from unittest.mock import patch, Mock
import os
from main import get_config, run_once

def test_get_config_default():
    """Test default configuration"""
    config = get_config()
    assert config['OPENSKY_URL'] == 'https://opensky-network.org/api/states/all'
    assert config['KAFKA_BOOTSTRAP_SERVERS'] == 'localhost:9092'
    assert config['KAFKA_TOPIC'] == 'flight-positions'
    assert config['KAFKA_LOGLEVEL'] == 'INFO'
    assert config['LAT_MIN'] == -33.75
    assert config['LAT_MAX'] == 5.27
    assert config['LON_MIN'] == -73.99
    assert config['LON_MAX'] == -34.79

def test_get_config_from_env():
    """Test configuration from environment variables"""
    env_vars = {
        'OPENSKY_URL': 'https://test-api.opensky-network.org/api/states/all',
        'KAFKA_BOOTSTRAP_SERVERS': 'test-broker:9092',
        'KAFKA_TOPIC': 'test-topic',
        'KAFKA_LOGLEVEL': 'DEBUG',
        'LAT_MIN': '-40.0',
        'LAT_MAX': '0.0',
        'LON_MIN': '-80.0',
        'LON_MAX': '-30.0'
    }
    
    with patch.dict(os.environ, env_vars):
        config = get_config()
        assert config['OPENSKY_URL'] == env_vars['OPENSKY_URL']
        assert config['KAFKA_BOOTSTRAP_SERVERS'] == env_vars['KAFKA_BOOTSTRAP_SERVERS']
        assert config['KAFKA_TOPIC'] == env_vars['KAFKA_TOPIC']
        assert config['KAFKA_LOGLEVEL'] == env_vars['KAFKA_LOGLEVEL']
        assert config['LAT_MIN'] == float(env_vars['LAT_MIN'])
        assert config['LAT_MAX'] == float(env_vars['LAT_MAX'])
        assert config['LON_MIN'] == float(env_vars['LON_MIN'])
        assert config['LON_MAX'] == float(env_vars['LON_MAX'])

@patch('main.OpenSkyClient')
@patch('main.EventProducer')
def test_run_once_with_kafka(mock_event_producer, mock_opensky_client, sample_config):
    """Test run_once with Kafka enabled"""
    # Mock flight data
    mock_flight_data = [{'icao24': 'abc123', 'callsign': 'TEST123'}]
    mock_opensky_client.return_value.process_flight_data.return_value = mock_flight_data
    
    # Run the function
    run_once(sample_config, print_mode=False)
    
    # Verify OpenSkyClient was called with correct parameters
    mock_opensky_client.assert_called_once_with(sample_config['OPENSKY_URL'])
    mock_opensky_client.return_value.process_flight_data.assert_called_once_with(
        sample_config['LAT_MIN'],
        sample_config['LAT_MAX'],
        sample_config['LON_MIN'],
        sample_config['LON_MAX'],
        print_mode=False
    )
    
    # Verify EventProducer was called with correct parameters
    mock_event_producer.assert_called_once_with(sample_config)
    mock_event_producer.return_value.submit_event.assert_called_once_with(mock_flight_data)

@patch('main.OpenSkyClient')
@patch('builtins.print')
def test_run_once_print_mode(mock_print, mock_opensky_client, sample_config):
    """Test run_once in print mode"""
    # Mock flight data
    mock_flight_data = [{'icao24': 'abc123', 'callsign': 'TEST123'}]
    mock_opensky_client.return_value.process_flight_data.return_value = mock_flight_data
    
    # Run the function
    run_once(sample_config, print_mode=True)
    
    # Verify OpenSkyClient was called with correct parameters
    mock_opensky_client.assert_called_once_with(sample_config['OPENSKY_URL'])
    mock_opensky_client.return_value.process_flight_data.assert_called_once_with(
        sample_config['LAT_MIN'],
        sample_config['LAT_MAX'],
        sample_config['LON_MIN'],
        sample_config['LON_MAX'],
        print_mode=True
    )
    
    # Verify print was called for each flight data
    assert mock_print.call_count == len(mock_flight_data) 