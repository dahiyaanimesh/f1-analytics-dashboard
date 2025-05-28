import fastf1
import pandas as pd
import numpy as np
import logging
import random

class DriverAnalyzer:
    """Handles driver performance analysis and comparisons"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Driver skill ratings database
        self.driver_skills = {
            'VER': {'consistency': 95, 'speed': 98, 'qualifying_performance': 92, 'race_craft': 96, 'wet_weather': 97, 'overtaking': 94},
            'LEC': {'consistency': 88, 'speed': 95, 'qualifying_performance': 97, 'race_craft': 90, 'wet_weather': 92, 'overtaking': 89},
            'HAM': {'consistency': 92, 'speed': 94, 'qualifying_performance': 89, 'race_craft': 98, 'wet_weather': 96, 'overtaking': 95},
            'RUS': {'consistency': 89, 'speed': 91, 'qualifying_performance': 93, 'race_craft': 87, 'wet_weather': 88, 'overtaking': 85},
            'NOR': {'consistency': 87, 'speed': 92, 'qualifying_performance': 88, 'race_craft': 85, 'wet_weather': 84, 'overtaking': 87},
            'PIA': {'consistency': 84, 'speed': 89, 'qualifying_performance': 86, 'race_craft': 82, 'wet_weather': 81, 'overtaking': 83},
            'SAI': {'consistency': 86, 'speed': 88, 'qualifying_performance': 85, 'race_craft': 87, 'wet_weather': 85, 'overtaking': 84},
            'PER': {'consistency': 82, 'speed': 86, 'qualifying_performance': 84, 'race_craft': 85, 'wet_weather': 83, 'overtaking': 81},
            'ALO': {'consistency': 91, 'speed': 90, 'qualifying_performance': 87, 'race_craft': 95, 'wet_weather': 93, 'overtaking': 92},
            'STR': {'consistency': 79, 'speed': 81, 'qualifying_performance': 78, 'race_craft': 80, 'wet_weather': 79, 'overtaking': 76},
            'ALB': {'consistency': 83, 'speed': 84, 'qualifying_performance': 82, 'race_craft': 83, 'wet_weather': 82, 'overtaking': 80},
            'OCO': {'consistency': 85, 'speed': 86, 'qualifying_performance': 83, 'race_craft': 86, 'wet_weather': 84, 'overtaking': 82},
            'HUL': {'consistency': 88, 'speed': 85, 'qualifying_performance': 86, 'race_craft': 87, 'wet_weather': 86, 'overtaking': 83},
            'TSU': {'consistency': 80, 'speed': 82, 'qualifying_performance': 81, 'race_craft': 79, 'wet_weather': 78, 'overtaking': 77},
            'LAW': {'consistency': 77, 'speed': 79, 'qualifying_performance': 78, 'race_craft': 76, 'wet_weather': 75, 'overtaking': 74},
            'GAS': {'consistency': 84, 'speed': 87, 'qualifying_performance': 85, 'race_craft': 84, 'wet_weather': 83, 'overtaking': 81},
            'DOO': {'consistency': 75, 'speed': 77, 'qualifying_performance': 76, 'race_craft': 74, 'wet_weather': 73, 'overtaking': 72},
            'MAG': {'consistency': 81, 'speed': 83, 'qualifying_performance': 80, 'race_craft': 82, 'wet_weather': 80, 'overtaking': 78},
            'BOT': {'consistency': 87, 'speed': 89, 'qualifying_performance': 88, 'race_craft': 86, 'wet_weather': 87, 'overtaking': 84},
            'ZHO': {'consistency': 76, 'speed': 78, 'qualifying_performance': 77, 'race_craft': 75, 'wet_weather': 74, 'overtaking': 73}
        }

    def analyze_driver_performance(self, driver_code, year=2025):
        """Analyze individual driver performance"""
        try:
            # Try to get real data first
            performance_data = self._get_real_driver_data(driver_code, year)
            if performance_data:
                return performance_data
            
            # Fall back to mock data
            return self._generate_mock_performance_data(driver_code, year)
            
        except Exception as e:
            self.logger.error(f"Error analyzing driver performance: {str(e)}")
            return self._generate_mock_performance_data(driver_code, year)

    def _get_real_driver_data(self, driver_code, year):
        """Try to get real driver data from FastF1"""
        try:
            # This would require loading multiple race sessions
            # For now, return None to use mock data
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting real driver data: {str(e)}")
            return None

    def _generate_mock_performance_data(self, driver_code, year):
        """Generate mock performance data for a driver"""
        # Get skill ratings
        skills = self.driver_skills.get(driver_code, {
            'consistency': random.randint(70, 85),
            'speed': random.randint(70, 85),
            'qualifying_performance': random.randint(70, 85),
            'race_craft': random.randint(70, 85),
            'wet_weather': random.randint(70, 85),
            'overtaking': random.randint(70, 85)
        })
        
        # Generate performance metrics based on skills
        base_performance = skills['speed'] / 10
        consistency_factor = skills['consistency'] / 100
        
        # Mock race results
        races = []
        total_points = 0
        total_positions_gained = 0
        q3_appearances = 0
        
        for race_num in range(1, min(25, 20)):  # Up to 24 races
            # Generate grid position based on qualifying skill
            grid_pos = max(1, min(20, int(np.random.normal(10 - skills['qualifying_performance']/10, 3))))
            if grid_pos <= 10:
                q3_appearances += 1
            
            # Generate race position based on various factors
            race_craft_bonus = (skills['race_craft'] - 80) / 100
            position_variance = 3 * (1 - consistency_factor)
            
            finish_pos = max(1, min(20, int(grid_pos + np.random.normal(race_craft_bonus, position_variance))))
            
            positions_gained = grid_pos - finish_pos
            total_positions_gained += positions_gained
            
            # Calculate points (F1 points system)
            points = 0
            if finish_pos == 1:
                points = 25
            elif finish_pos == 2:
                points = 18
            elif finish_pos == 3:
                points = 15
            elif finish_pos == 4:
                points = 12
            elif finish_pos == 5:
                points = 10
            elif finish_pos == 6:
                points = 8
            elif finish_pos == 7:
                points = 6
            elif finish_pos == 8:
                points = 4
            elif finish_pos == 9:
                points = 2
            elif finish_pos == 10:
                points = 1
            
            total_points += points
            
            race_data = {
                'race_name': f'Race {race_num}',
                'position': finish_pos,
                'grid_position': grid_pos,
                'positions_gained': positions_gained,
                'points': points
            }
            races.append(race_data)
        
        # Calculate averages
        avg_race_pos = np.mean([r['position'] for r in races])
        avg_qual_pos = np.mean([r['grid_position'] for r in races])
        
        return {
            'overall_metrics': {
                'average_race_position': avg_race_pos,
                'average_qualifying_position': avg_qual_pos,
                'total_points': total_points,
                'total_positions_gained': total_positions_gained,
                'position_consistency': consistency_factor * 100,
                'q3_appearances': q3_appearances,
                'races_completed': len(races),
                'total_races': len(races)
            },
            'skill_ratings': skills,
            'races': races
        }

    def compare_drivers(self, driver_codes, year=2025):
        """Compare multiple drivers"""
        try:
            comparison_data = {
                'drivers': driver_codes,
                'metrics_comparison': {},
                'skill_ratings': {}
            }
            
            # Get data for each driver
            driver_data = {}
            for driver in driver_codes:
                driver_data[driver] = self.analyze_driver_performance(driver, year)
            
            # Extract metrics for comparison
            metrics = ['average_race_position', 'average_qualifying_position', 'total_points', 'total_positions_gained']
            for metric in metrics:
                comparison_data['metrics_comparison'][metric] = {}
                for driver in driver_codes:
                    if driver in driver_data and driver_data[driver]:
                        comparison_data['metrics_comparison'][metric][driver] = driver_data[driver]['overall_metrics'].get(metric, 0)
                    else:
                        comparison_data['metrics_comparison'][metric][driver] = 0
            
            # Extract skill ratings for comparison
            skills = ['consistency', 'speed', 'qualifying_performance', 'race_craft', 'wet_weather', 'overtaking']
            for skill in skills:
                comparison_data['skill_ratings'][skill] = {}
                for driver in driver_codes:
                    if driver in driver_data and driver_data[driver]:
                        comparison_data['skill_ratings'][skill][driver] = driver_data[driver]['skill_ratings'].get(skill, 0)
                    else:
                        comparison_data['skill_ratings'][skill][driver] = 0
            
            return comparison_data
            
        except Exception as e:
            self.logger.error(f"Error comparing drivers: {str(e)}")
            return {
                'drivers': driver_codes,
                'metrics_comparison': {},
                'skill_ratings': {}
            } 