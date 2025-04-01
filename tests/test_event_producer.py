import pytest
import json
from events.event_producer import EventProducer

def test_event_producer_initialization(sample_config):
    """Test EventProducer initialization"""
    producer = EventProducer(sample_config)
    assert producer.config == sample_config

def test_submit_event(sample_config, sample_flight_data, mock_kafka_producer):
    """Test event submission to Kafka"""
    producer = EventProducer(sample_config)
    
    producer.submit_event(sample_flight_data)
    
    # Verify that produce was called for each flight data
    assert mock_kafka_producer.produce.call_count == len(sample_flight_data)
    
    # Verify the produce calls with correct arguments
    for i, flight_data in enumerate(sample_flight_data):
        call_args = mock_kafka_producer.produce.call_args_list[i][1]
        assert call_args['topic'] == sample_config['KAFKA_TOPIC']
        assert call_args['key'] == flight_data['icao24']
        assert json.loads(call_args['value']) == flight_data

def test_submit_event_empty_data(sample_config, mock_kafka_producer):
    """Test event submission with empty data"""
    producer = EventProducer(sample_config)
    
    producer.submit_event([])
    
    # Verify that produce was not called
    mock_kafka_producer.produce.assert_not_called() 