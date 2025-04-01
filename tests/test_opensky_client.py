import pytest
from unittest.mock import patch, Mock
from opensky.opensky_client import OpenSkyClient

def test_opensky_client_initialization():
    """Test OpenSkyClient initialization"""
    url = "https://test-api.opensky-network.org/api/states/all"
    client = OpenSkyClient(url)
    assert client.url == url

@patch('requests.get')
def test_fetch_flight_positions_success(mock_get, mock_response):
    """Test successful flight positions fetch"""
    mock_get.return_value = mock_response
    client = OpenSkyClient("https://test-api.opensky-network.org/api/states/all")
    
    result = client._OpenSkyClient__fetch_flight_positions(-33.75, 5.27, -73.99, -34.79)
    
    assert result == mock_response.json.return_value
    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs['params']['lamin'] == -33.75
    assert kwargs['params']['lamax'] == 5.27
    assert kwargs['params']['lomin'] == -73.99
    assert kwargs['params']['lomax'] == -34.79

@patch('requests.get')
def test_fetch_flight_positions_error(mock_get):
    """Test flight positions fetch with error"""
    mock_get.side_effect = Exception("API Error")
    client = OpenSkyClient("https://test-api.opensky-network.org/api/states/all")
    
    result = client._OpenSkyClient__fetch_flight_positions(-33.75, 5.27, -73.99, -34.79)
    
    assert result == []

@patch('requests.get')
def test_process_flight_data_success(mock_get, mock_response):
    """Test successful flight data processing"""
    mock_get.return_value = mock_response
    client = OpenSkyClient("https://test-api.opensky-network.org/api/states/all")
    
    result = client.process_flight_data(-33.75, 5.27, -73.99, -34.79)
    
    assert len(result) == 1
    flight_data = result[0]
    assert flight_data['icao24'] == 'abc123'
    assert flight_data['callsign'] == 'TEST123'
    assert flight_data['origin_country'] == 'Brazil'
    assert flight_data['longitude'] == -45.0
    assert flight_data['latitude'] == -23.0
    assert flight_data['altitude'] == 10000.0
    assert flight_data['on_ground'] is False
    assert flight_data['velocity'] == 200.0
    assert flight_data['true_track'] == 180.0
    assert flight_data['vertical_rate'] == 0.0
    assert flight_data['geo_altitude'] == 10000.0
    assert flight_data['squawk'] == '1234'

@patch('requests.get')
def test_process_flight_data_empty_response(mock_get):
    """Test flight data processing with empty response"""
    mock_get.return_value = Mock(json=lambda: {'states': []})
    client = OpenSkyClient("https://test-api.opensky-network.org/api/states/all")
    
    result = client.process_flight_data(-33.75, 5.27, -73.99, -34.79)
    
    assert result == []

@patch('requests.get')
def test_process_flight_data_invalid_response(mock_get):
    """Test flight data processing with invalid response"""
    mock_get.return_value = Mock(json=lambda: {})
    client = OpenSkyClient("https://test-api.opensky-network.org/api/states/all")
    
    result = client.process_flight_data(-33.75, 5.27, -73.99, -34.79)
    
    assert result == []

@patch('requests.get')
def test_process_flight_data_with_none_state(mock_get):
    """Test flight data processing with None state"""
    mock_get.return_value = Mock(json=lambda: {'states': [None]})
    client = OpenSkyClient("https://test-api.opensky-network.org/api/states/all")
    
    result = client.process_flight_data(-33.75, 5.27, -73.99, -34.79)
    
    assert result == [] 