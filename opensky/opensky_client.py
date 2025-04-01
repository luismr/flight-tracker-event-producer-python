import requests
import json
from datetime import datetime


class OpenSkyClient:
    """
    OpenSkyClient is a class that fetches flight positions from the OpenSky Network API.
    """

    def __init__(self, url: str):
        self.url = url

    def __fetch_flight_positions(self, lat_min: float, lat_max: float, lon_min: float, lon_max: float) -> list[dict]:
        """
        Fetch flight positions from the OpenSky Network API within a specified bounding box.

        Args:
            lat_min (float): The minimum latitude of the bounding box.
            lat_max (float): The maximum latitude of the bounding box.
            lon_min (float): The minimum longitude of the bounding box.
            lon_max (float): The maximum longitude of the bounding box.

        Returns:
            list[dict]: A list of dictionaries containing flight position data.
        """
        
        params = {
            'lamin': lat_min,
            'lamax': lat_max,
            'lomin': lon_min,
            'lomax': lon_max
        }

        try:
            response = requests.get(self.url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching flight positions: {e}")
            return []
        
    def process_flight_data(self, lat_min: float, lat_max: float, lon_min: float, lon_max: float, print_mode=False) -> list:
        """Process flight data and either print to stdout or return for Kafka publishing.

        Args:
            lat_min (float): The minimum latitude of the bounding box.
            lat_max (float): The maximum latitude of the bounding box.
            lon_min (float): The minimum longitude of the bounding box.
            lon_max (float): The maximum longitude of the bounding box.
        """

        data = self.__fetch_flight_positions(lat_min, lat_max, lon_min, lon_max);    
        if not data or 'states' not in data:
            return [] if not print_mode else None
        
        timestamp = datetime.now().isoformat()
        processed_data = []
        
        for state in data['states']:
            if state is None:
                continue
                
            # OpenSky Network API response format:
            # [icao24, callsign, origin_country, time_position, time_velocity, longitude, latitude, altitude, on_ground, velocity, true_track, vertical_rate, sensors, geo_altitude, squawk, spi, position_source]
            flight_data = {
                'timestamp': timestamp,
                'icao24': state[0],
                'callsign': state[1].strip() if state[1] else None,
                'origin_country': state[2],
                'longitude': state[5],
                'latitude': state[6],
                'altitude': state[7],
                'on_ground': state[8],
                'velocity': state[9],
                'true_track': state[10],
                'vertical_rate': state[11],
                'geo_altitude': state[13],
                'squawk': state[14]
            }
            
            if print_mode:
                print(json.dumps(flight_data, indent=2))
            else:
                processed_data.append(flight_data)
        
        return processed_data if not print_mode else None