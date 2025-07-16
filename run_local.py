#!/usr/bin/env python3
"""
Local development script for National Rail Departure Board
"""

import os
import sys
import subprocess
import time
import requests

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import requests
        print("✅ Dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def create_test_config():
    """Create a test configuration file"""
    config = {
        'api_key': '',
        'start_station': 'PAD',
        'destination_station': '',
        'refresh_interval': 60,
        'max_departures': 10,
        'time_window': 120
    }
    
    # Create /data directory if it doesn't exist
    os.makedirs('/data', exist_ok=True)
    
    # Write test config
    with open('/data/options.json', 'w') as f:
        import json
        json.dump(config, f, indent=2)
    
    print("✅ Test configuration created")

def run_app():
    """Run the Flask application"""
    print("🚂 Starting National Rail Departure Board...")
    print("📍 Access the app at: http://localhost:8123")
    print("🔄 Press Ctrl+C to stop")
    print()
    
    try:
        # Run the Flask app
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

def main():
    """Main function"""
    print("=" * 50)
    print("National Rail Departure Board - Local Development")
    print("=" * 50)
    print()
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Create test config
    create_test_config()
    
    # Run the app
    run_app()

if __name__ == "__main__":
    main() 