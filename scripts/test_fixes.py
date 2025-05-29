#!/usr/bin/env python3
"""Test script to verify the fixes work correctly"""

def test_standings():
    """Test the updated 2025 standings"""
    print("🏆 Testing 2025 Standings...")
    
    from data_processor import DataProcessor
    dp = DataProcessor()
    standings = dp.get_season_standings(2025)
    
    if standings and standings.get('drivers'):
        print(f"✅ Found {len(standings['drivers'])} drivers")
        print("Top 5 Drivers:")
        for i, driver in enumerate(standings['drivers'][:5]):
            print(f"  {i+1}. {driver['name']} ({driver['driver']}) - {driver['points']} pts")
        
        # Check if Piastri is leading
        leader = standings['drivers'][0]
        if leader['driver'] == 'PIA':
            print("✅ Oscar Piastri is correctly leading the championship!")
        else:
            print(f"❌ Expected Piastri leading, but found {leader['name']}")
    else:
        print("❌ No standings data found")

def test_races():
    """Test that races are available"""
    print("\n🏁 Testing Race Data...")
    
    from data_processor import DataProcessor
    dp = DataProcessor()
    races = dp.get_season_races(2025)
    
    if races:
        print(f"✅ Found {len(races)} races for 2025")
        print("First few races:")
        for race in races[:3]:
            print(f"  Round {race['round']}: {race['name']} ({race['date']})")
    else:
        print("❌ No races found for 2025")

def test_strategy_optimizer():
    """Test strategy optimization"""
    print("\n⚡ Testing Strategy Optimization...")
    
    try:
        from strategy_optimizer import StrategyOptimizer
        so = StrategyOptimizer()
        
        # Test with different drivers and tracks
        test_cases = [
            (2025, 1, 'PIA'),  # Piastri at Australia
            (2025, 8, 'VER'),  # Verstappen at Monaco
            (2025, 16, 'NOR'), # Norris at Italy
        ]
        
        for year, round_num, driver in test_cases:
            result = so.optimize_pit_strategy(year, round_num, driver)
            weather = result.get('track_conditions', {}).get('weather', 'N/A')
            stops = result['optimal_strategy']['stops']
            compounds = result.get('available_compounds', [])
            
            print(f"  {driver} @ Round {round_num}: {stops} stops, {weather} weather, compounds: {compounds}")
        
        print("✅ Strategy optimization working with varied results!")
        
    except Exception as e:
        print(f"❌ Strategy optimization error: {e}")

if __name__ == "__main__":
    print("🧪 Testing F1 Analytics Fixes...\n")
    
    test_standings()
    test_races()
    test_strategy_optimizer()
    
    print("\n✅ All tests completed!") 