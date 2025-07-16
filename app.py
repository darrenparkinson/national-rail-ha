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

# Configuration
CONFIG_FILE = '/data/options.json'

def load_config():
    """Load configuration from Home Assistant"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {
        'api_key': '',
        'start_station': 'PAD',
        'destination_station': '',
        'refresh_interval': 60,
        'max_departures': 10,
        'time_window': 120
    }

def load_stations():
    """Load station data"""
    try:
        with open('stations.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
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
        return get_mock_departures()
    
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
            return parse_national_rail_response(data)
        else:
            print(f"API Error: {response.status_code}")
            return get_mock_departures()
            
    except Exception as e:
        print(f"Error fetching departures: {e}")
        return get_mock_departures()

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
    config = load_config()
    stations = load_stations()
    return render_template('index.html', config=config, stations=stations)

@app.route('/api/departures')
def api_departures():
    """API endpoint for departure data"""
    config = load_config()
    
    station_code = request.args.get('station', config.get('start_station', 'PAD'))
    destination_code = request.args.get('destination', config.get('destination_station', ''))
    max_rows = int(request.args.get('max_rows', config.get('max_departures', 10)))
    
    departures = get_national_rail_departures(
        config.get('api_key', ''),
        station_code,
        destination_code,
        max_rows
    )
    
    return jsonify({
        'departures': departures,
        'station': station_code,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stations')
def api_stations():
    """API endpoint for station data"""
    stations = load_stations()
    return jsonify(stations)

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8123, debug=False) 