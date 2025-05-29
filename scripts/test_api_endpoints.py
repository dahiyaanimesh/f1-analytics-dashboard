#!/usr/bin/env python3
"""Test API endpoints to verify fixes are working"""

import requests
import json

def test_api_endpoint(url, description):
    """Test an API endpoint"""
    try:
        print(f"\n🧪 Testing {description}...")
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ {description} - SUCCESS")
            return data
        else:
            print(f"❌ {description} - FAILED: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ {description} - ERROR: {str(e)}")
        return None

def test_standings():
    """Test standings data"""
    data = test_api_endpoint("http://localhost:5000/api/season-standings/2025", "2025 Standings")
    
    if data and data.get('success') and data.get('data'):
        drivers = data['data']['drivers']
        print(f"📊 Found {len(drivers)} drivers in standings")
        
        print("\nTop 5 drivers:")
        for i, driver in enumerate(drivers[:5]):
            print(f"  {i+1}. {driver['name']} ({driver['driver']}) - {driver['points']} pts")
        
        # Check if Bottas or Perez are present
        driver_codes = [d['driver'] for d in drivers]
        if 'BOT' in driver_codes:
            print("❌ ERROR: Bottas (BOT) still found in 2025 standings!")
        else:
            print("✅ Bottas correctly removed from 2025 standings")
            
        if 'PER' in driver_codes:
            print("❌ ERROR: Perez (PER) still found in 2025 standings!")
        else:
            print("✅ Perez correctly removed from 2025 standings")
        
        # Check for new drivers
        new_drivers = ['LAW', 'COL', 'BEA', 'ANT', 'HAD', 'DOO']
        found_new = [code for code in new_drivers if code in driver_codes]
        print(f"✅ New 2025 drivers found: {found_new}")
        
    return data

def test_races():
    """Test races data"""
    data = test_api_endpoint("http://localhost:5000/api/races?year=2025", "2025 Race Calendar")
    
    if data and data.get('success') and data.get('data'):
        races = data['data']
        print(f"🏁 Found {len(races)} races for 2025")
        
        if len(races) > 0:
            print("\nFirst 3 races:")
            for race in races[:3]:
                print(f"  Round {race['round']}: {race['name']} - {race['date']}")
            print("✅ Race rounds are visible and working")
        else:
            print("❌ No races found!")
    
    return data

if __name__ == "__main__":
    print("🏎️  Testing F1 Analytics API Endpoints...")
    
    # Test health check first
    health = test_api_endpoint("http://localhost:5000/api/health", "Health Check")
    
    if health and health.get('status') == 'healthy':
        print("✅ Backend is healthy, proceeding with tests...")
        
        # Test the main issues
        test_standings()
        test_races()
        
        print("\n✅ API endpoint testing completed!")
    else:
        print("❌ Backend is not healthy or not running. Please start with: python app.py") 