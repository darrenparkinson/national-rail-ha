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
        # Home Assistant ingress paths are typically like /b2161d7a_national-rail-departure-board/ingress
        # We want to extract the base part without /ingress
        path = request.path
        if '/ingress' in path:
            # Remove /ingress and get the base path
            base_path = path.replace('/ingress', '').rstrip('/')
            if base_path:
                ingress_path = base_path
    
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
CONFIG_FILE = '/data/options.json'

# Add debug logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    """Load configuration from Home Assistant"""
    logger.info(f"Loading config from: {CONFIG_FILE}")
    
    # Try to read existing config
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                logger.info(f"Loaded config: {config}")
                return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
    
    logger.info("Config file not found or unreadable, using defaults")
    
    default_config = {
        'api_key': '',
        'start_station': 'PAD',
        'destination_station': '',
        'refresh_interval': 60,
        'max_departures': 10,
        'time_window': 120
    }
    
    # Try to create a default config file (but don't fail if we can't)
    try:
        # Ensure /data directory exists
        data_dir = os.path.dirname(CONFIG_FILE)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir, exist_ok=True)
            logger.info(f"Created data directory: {data_dir}")
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=2)
        logger.info(f"Created default config file: {CONFIG_FILE}")
    except Exception as e:
        logger.warning(f"Could not create config file (this is normal): {e}")
    
    logger.info(f"Using default config: {default_config}")
    return default_config

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
    if not api_key:
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
        config = load_config()
        stations = load_stations()
        logger.info(f"Rendering template with {len(stations)} stations")
        return render_template('index.html', config=config, stations=stations, get_base_url=get_base_url)
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        return f"Error: {str(e)}", 500

@app.route('/api/departures')
def api_departures():
    """API endpoint for departure data"""
    try:
        logger.info("API departures called")
        config = load_config()
        
        station_code = request.args.get('station', config.get('start_station', 'PAD'))
        destination_code = request.args.get('destination', config.get('destination_station', ''))
        max_rows = int(request.args.get('max_rows', config.get('max_departures', 10)))
        
        logger.info(f"Getting departures for station: {station_code}")
        departures, is_mock_data = get_national_rail_departures(
            config.get('api_key', ''),
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
        return jsonify({
            'status': 'healthy', 
            'timestamp': datetime.now().isoformat(),
            'config_loaded': os.path.exists(CONFIG_FILE),
            'stations_loaded': len(load_stations()),
            'ingress_path': get_ingress_path(),
            'base_url': get_base_url()
        })
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8124, debug=False) 