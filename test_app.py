#!/usr/bin/env python3
"""
Test script for National Rail Departure Board
"""

import requests
import json
import time

def test_app():
    """Test the application endpoints"""
    base_url = "http://localhost:8123"
    
    print("Testing National Rail Departure Board...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False
    
    # Test stations endpoint
    try:
        response = requests.get(f"{base_url}/api/stations", timeout=5)
        if response.status_code == 200:
            stations = response.json()
            print(f"✅ Stations endpoint working: {len(stations)} stations loaded")
        else:
            print(f"❌ Stations endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Stations endpoint error: {e}")
    
    # Test departures endpoint
    try:
        response = requests.get(f"{base_url}/api/departures?station=PAD", timeout=5)
        if response.status_code == 200:
            data = response.json()
            departures = data.get('departures', [])
            print(f"✅ Departures endpoint working: {len(departures)} departures loaded")
            
            # Show first departure details
            if departures:
                first = departures[0]
                print(f"   Sample departure: {first.get('destination')} at {first.get('estimated_departure')}")
        else:
            print(f"❌ Departures endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Departures endpoint error: {e}")
    
    # Test main page
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Main page accessible")
        else:
            print(f"❌ Main page failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Main page error: {e}")
    
    print("\n🎉 Testing complete!")
    return True

if __name__ == "__main__":
    test_app() 