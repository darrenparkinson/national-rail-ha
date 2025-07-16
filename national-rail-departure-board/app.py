#!/usr/bin/env python3
"""
National Rail Departure Board - Home Assistant Add-on
A beautiful departure board for UK railway stations using National Rail data
"""

import os
import json
import time
import requests
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Handle Home Assistant ingress
def get_ingress_path():
    """Get the ingress path from environment variables"""
    # Check for Home Assistant ingress path
    ingress_path = os.environ.get('SUPERVISOR_INGRESS_PATH', '')
    
    # If no environment variable, try to detect from request
    if not ingress_path and hasattr(request, 'path'):
        # Home Assistant ingress paths are variable: /{unique_id}_addon_name/ingress
        # We want to extract the base part without /ingress
        path = request.path
        logger.info(f"Request path: {path}")
        
        if '/ingress' in path:
            # Remove /ingress and get the base path
            base_path = path.replace('/ingress', '').rstrip('/')
            if base_path:
                ingress_path = base_path
                logger.info(f"Detected ingress path: {ingress_path}")
        else:
            # If no /ingress, use the full path
            ingress_path = path.rstrip('/')
            logger.info(f"Using full path as ingress: {ingress_path}")
    
    return ingress_path

def get_base_url():
    """Get the base URL for static files"""
    ingress_path = get_ingress_path()
    logger.info(f"Ingress path: '{ingress_path}'")
    if ingress_path:
        base_url = ingress_path.rstrip('/')
        logger.info(f"Base URL: '{base_url}'")
        return base_url
    logger.info("No ingress path, using empty base URL")
    return ''

# Configuration
# CONFIG_FILE = '/data/options.json' # Removed as per edit hint

# Add debug logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Remove load_config and instead use environment variables throughout the app
# Example usage:
# api_key = os.environ.get('API_KEY', '')
# start_station = os.environ.get('START_STATION', 'PAD')
# destination_station = os.environ.get('DESTINATION_STATION', '')
# refresh_interval = int(os.environ.get('REFRESH_INTERVAL', 60))
# max_departures = int(os.environ.get('MAX_DEPARTURES', 10))
# time_window = int(os.environ.get('TIME_WINDOW', 120))

def load_stations():
    """Load station data"""
    try:
        logger.info("Loading stations.json")
        with open('stations.json', 'r') as f:
            stations = json.load(f)
            logger.info(f"Loaded {len(stations)} stations")
            return stations
    except FileNotFoundError:
        logger.error("stations.json not found")
        return []
    except Exception as e:
        logger.error(f"Error loading stations: {e}")
        return []

def get_mock_departures():
    """Generate mock departure data for testing"""
    now = datetime.now()
    mock_departures = []
    
    destinations = [
        {'name': 'London Paddington', 'crs': 'PAD', 'operator': 'GWR'},
        {'name': 'London Waterloo', 'crs': 'WAT', 'operator': 'SWR'},
        {'name': 'London Victoria', 'crs': 'VIC', 'operator': 'Southern'},
        {'name': 'London Bridge', 'crs': 'LBG', 'operator': 'Thameslink'},
        {'name': 'Reading', 'crs': 'RDG', 'operator': 'GWR'},
        {'name': 'Bristol Temple Meads', 'crs': 'BRI', 'operator': 'GWR'},
        {'name': 'Cardiff Central', 'crs': 'CDF', 'operator': 'GWR'},
        {'name': 'Manchester Piccadilly', 'crs': 'MAN', 'operator': 'Avanti West Coast'},
        {'name': 'Birmingham New Street', 'crs': 'BHM', 'operator': 'Avanti West Coast'},
        {'name': 'Edinburgh Waverley', 'crs': 'EDB', 'operator': 'LNER'}
    ]
    
    for i, dest in enumerate(destinations):
        # Create staggered departure times
        departure_time = now + timedelta(minutes=15 + (i * 10))
        
        # Random platform
        platform = f"{i % 4 + 1}{'A' if i % 2 == 0 else 'B'}"
        
        # Random status
        statuses = ['On Time', 'Delayed', 'Cancelled', 'Platform Change']
        status = statuses[i % len(statuses)]
        
        mock_departures.append({
            'destination': dest['name'],
            'destination_crs': dest['crs'],
            'operator': dest['operator'],
            'scheduled_departure': departure_time.strftime('%H:%M'),
            'estimated_departure': departure_time.strftime('%H:%M'),
            'platform': platform,
            'status': status,
            'delay': i % 3 * 5 if status == 'Delayed' else 0,
            'cancelled': status == 'Cancelled'
        })
    
    return mock_departures

def get_national_rail_departures(api_key, station_code, destination_code=None, max_rows=10):
    """Get real departure data from National Rail API"""
    logger.info(f"get_national_rail_departures called with api_key: {bool(api_key)}")
    if not api_key:
        logger.info("No API key provided, using mock data")
        return get_mock_departures(), True  # Return mock data and flag indicating it's mock
    
    try:
        # National Rail API endpoint
        url = f"https://api.departureboard.io/v2.0/GetDepartureBoard/{station_code}"
        
        params = {
            'numRows': max_rows,
            'timeWindow': 120
        }
        
        if destination_code:
            params['filterCrs'] = destination_code
            params['filterType'] = 'to'
        
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            return parse_national_rail_response(data), False  # Real data
        else:
            print(f"API Error: {response.status_code}")
            return get_mock_departures(), True  # Fallback to mock data
            
    except Exception as e:
        print(f"Error fetching departures: {e}")
        return get_mock_departures(), True  # Fallback to mock data

def parse_national_rail_response(data):
    """Parse National Rail API response"""
    departures = []
    
    try:
        board = data.get('GetStationBoardResult', {})
        train_services = board.get('trainServices', {}).get('service', [])
        
        if not isinstance(train_services, list):
            train_services = [train_services]
        
        for service in train_services:
            departure = {
                'destination': service.get('destination', {}).get('location', {}).get('locationName', 'Unknown'),
                'destination_crs': service.get('destination', {}).get('location', {}).get('crs', ''),
                'operator': service.get('operator', 'Unknown'),
                'scheduled_departure': service.get('std', ''),
                'estimated_departure': service.get('etd', ''),
                'platform': service.get('platform', 'TBC'),
                'status': service.get('etd', 'On Time'),
                'delay': 0,
                'cancelled': service.get('etd') == 'Cancelled'
            }
            
            # Calculate delay
            if departure['scheduled_departure'] and departure['estimated_departure']:
                try:
                    scheduled = datetime.strptime(departure['scheduled_departure'], '%H:%M')
                    estimated = datetime.strptime(departure['estimated_departure'], '%H:%M')
                    delay_minutes = (estimated - scheduled).total_seconds() / 60
                    departure['delay'] = int(delay_minutes)
                except:
                    departure['delay'] = 0
            
            departures.append(departure)
    
    except Exception as e:
        print(f"Error parsing API response: {e}")
        return get_mock_departures()
    
    return departures

@app.route('/')
def index():
    """Main departure board page"""
    try:
        logger.info("Loading main page")
        # config = load_config() # Removed as per edit hint
        # stations = load_stations() # Removed as per edit hint
        # logger.info(f"Rendering template with {len(stations)} stations") # Removed as per edit hint
        return render_template('index.html') # Removed as per edit hint
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return f"Error: {str(e)}", 500

@app.route('/api/departures')
def api_departures():
    """API endpoint for departure data"""
    try:
        logger.info("API departures called")
        # config = load_config() # Removed as per edit hint
        
        station_code = request.args.get('station', os.environ.get('START_STATION', 'PAD')) # Changed to use env var
        destination_code = request.args.get('destination', os.environ.get('DESTINATION_STATION', '')) # Changed to use env var
        max_rows = int(request.args.get('max_rows', os.environ.get('MAX_DEPARTURES', 10))) # Changed to use env var
        
        logger.info(f"Getting departures for station: {station_code}")
        api_key = os.environ.get('API_KEY', '') # Changed to use env var
        logger.info(f"API key present: {bool(api_key)}")
        if api_key:
            logger.info(f"API key length: {len(api_key)}")
        
        departures, is_mock_data = get_national_rail_departures(
            api_key,
            station_code,
            destination_code,
            max_rows
        )
        
        logger.info(f"Returning {len(departures)} departures (mock: {is_mock_data})")
        response = {
            'departures': departures,
            'station': station_code,
            'timestamp': datetime.now().isoformat(),
            'is_mock_data': is_mock_data
        }
        logger.info(f"Response: {response}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in departures API: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/stations')
def api_stations():
    """API endpoint for station data"""
    try:
        logger.info("API stations called")
        stations = load_stations()
        logger.info(f"Returning {len(stations)} stations")
        return jsonify(stations)
    except Exception as e:
        logger.error(f"Error in stations API: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        logger.info("Health check called")
        current_path = request.path if hasattr(request, 'path') else 'unknown'
        return jsonify({
            'status': 'healthy', 
            'timestamp': datetime.now().isoformat(),
            'config_loaded': os.path.exists(CONFIG_FILE), # This line was not in the edit hint, so it remains
            'stations_loaded': len(load_stations()),
            'ingress_path': get_ingress_path(),
            'base_url': get_base_url(),
            'current_path': current_path,
            'environment': {
                'SUPERVISOR_INGRESS_PATH': os.environ.get('SUPERVISOR_INGRESS_PATH', 'not_set')
            }
        })
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/debug')
def debug():
    """Debug endpoint to see request details"""
    try:
        return jsonify({
            'path': request.path,
            'url': request.url,
            'base_url': request.base_url,
            'host': request.host,
            'headers': dict(request.headers),
            'ingress_path': get_ingress_path(),
            'base_url_func': get_base_url()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8124, debug=False) 