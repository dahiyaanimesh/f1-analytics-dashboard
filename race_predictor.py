import pandas as pd
import numpy as np
import logging
import random
from datetime import datetime, timedelta
import fastf1
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class EnhancedRacePredictor:
    """Enhanced race outcome predictor using ML models and comprehensive data analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize models
        self.position_model = None
        self.win_probability_model = None
        self.podium_probability_model = None
        self.points_probability_model = None
        self.scaler = StandardScaler()
        
        # Comprehensive driver ratings (updated for 2025)
        self.driver_ratings = {
            'VER': {
                'skill': 98, 'consistency': 95, 'race_craft': 96, 'qualifying': 92,
                'wet_weather': 97, 'overtaking': 94, 'tire_management': 95,
                'pressure_handling': 97, 'championship_experience': 98
            },
            'LEC': {
                'skill': 95, 'consistency': 88, 'race_craft': 90, 'qualifying': 97,
                'wet_weather': 92, 'overtaking': 89, 'tire_management': 88,
                'pressure_handling': 89, 'championship_experience': 85
            },
            'HAM': {
                'skill': 96, 'consistency': 92, 'race_craft': 98, 'qualifying': 89,
                'wet_weather': 96, 'overtaking': 95, 'tire_management': 94,
                'pressure_handling': 98, 'championship_experience': 99
            },
            'RUS': {
                'skill': 91, 'consistency': 89, 'race_craft': 87, 'qualifying': 93,
                'wet_weather': 88, 'overtaking': 85, 'tire_management': 86,
                'pressure_handling': 87, 'championship_experience': 75
            },
            'NOR': {
                'skill': 90, 'consistency': 87, 'race_craft': 85, 'qualifying': 88,
                'wet_weather': 84, 'overtaking': 87, 'tire_management': 86,
                'pressure_handling': 85, 'championship_experience': 80
            },
            'PIA': {
                'skill': 87, 'consistency': 84, 'race_craft': 82, 'qualifying': 86,
                'wet_weather': 81, 'overtaking': 83, 'tire_management': 84,
                'pressure_handling': 82, 'championship_experience': 70
            },
            'SAI': {
                'skill': 88, 'consistency': 86, 'race_craft': 87, 'qualifying': 85,
                'wet_weather': 85, 'overtaking': 84, 'tire_management': 87,
                'pressure_handling': 86, 'championship_experience': 82
            },
            'ALO': {
                'skill': 93, 'consistency': 91, 'race_craft': 95, 'qualifying': 87,
                'wet_weather': 93, 'overtaking': 92, 'tire_management': 94,
                'pressure_handling': 95, 'championship_experience': 95
            },
            'STR': {
                'skill': 78, 'consistency': 79, 'race_craft': 80, 'qualifying': 78,
                'wet_weather': 79, 'overtaking': 76, 'tire_management': 78,
                'pressure_handling': 75, 'championship_experience': 78
            },
            'ALB': {
                'skill': 84, 'consistency': 83, 'race_craft': 83, 'qualifying': 82,
                'wet_weather': 82, 'overtaking': 80, 'tire_management': 83,
                'pressure_handling': 81, 'championship_experience': 77
            },
            'OCO': {
                'skill': 85, 'consistency': 85, 'race_craft': 86, 'qualifying': 83,
                'wet_weather': 84, 'overtaking': 82, 'tire_management': 85,
                'pressure_handling': 83, 'championship_experience': 79
            },
            'HUL': {
                'skill': 86, 'consistency': 88, 'race_craft': 87, 'qualifying': 86,
                'wet_weather': 86, 'overtaking': 83, 'tire_management': 87,
                'pressure_handling': 84, 'championship_experience': 82
            },
            'TSU': {
                'skill': 81, 'consistency': 80, 'race_craft': 79, 'qualifying': 81,
                'wet_weather': 78, 'overtaking': 77, 'tire_management': 79,
                'pressure_handling': 78, 'championship_experience': 74
            },
            'LAW': {
                'skill': 78, 'consistency': 77, 'race_craft': 76, 'qualifying': 78,
                'wet_weather': 75, 'overtaking': 74, 'tire_management': 76,
                'pressure_handling': 75, 'championship_experience': 70
            },
            'GAS': {
                'skill': 86, 'consistency': 84, 'race_craft': 84, 'qualifying': 85,
                'wet_weather': 83, 'overtaking': 81, 'tire_management': 84,
                'pressure_handling': 82, 'championship_experience': 78
            },
            'DOO': {
                'skill': 76, 'consistency': 75, 'race_craft': 74, 'qualifying': 76,
                'wet_weather': 73, 'overtaking': 72, 'tire_management': 74,
                'pressure_handling': 72, 'championship_experience': 65
            },
            'MAG': {
                'skill': 82, 'consistency': 81, 'race_craft': 82, 'qualifying': 80,
                'wet_weather': 80, 'overtaking': 78, 'tire_management': 81,
                'pressure_handling': 79, 'championship_experience': 76
            },
            'BOT': {
                'skill': 87, 'consistency': 87, 'race_craft': 86, 'qualifying': 88,
                'wet_weather': 87, 'overtaking': 84, 'tire_management': 86,
                'pressure_handling': 85, 'championship_experience': 85
            },
            'ZHO': {
                'skill': 77, 'consistency': 76, 'race_craft': 75, 'qualifying': 77,
                'wet_weather': 74, 'overtaking': 73, 'tire_management': 75,
                'pressure_handling': 74, 'championship_experience': 72
            },
            'ANT': {  # Kimi Antonelli
                'skill': 83, 'consistency': 78, 'race_craft': 76, 'qualifying': 85,
                'wet_weather': 79, 'overtaking': 77, 'tire_management': 80,
                'pressure_handling': 75, 'championship_experience': 60
            },
            'HAD': {  # Isack Hadjar
                'skill': 79, 'consistency': 76, 'race_craft': 74, 'qualifying': 80,
                'wet_weather': 75, 'overtaking': 73, 'tire_management': 77,
                'pressure_handling': 73, 'championship_experience': 65
            },
            'COL': {  # Franco Colapinto
                'skill': 77, 'consistency': 74, 'race_craft': 72, 'qualifying': 78,
                'wet_weather': 73, 'overtaking': 71, 'tire_management': 75,
                'pressure_handling': 71, 'championship_experience': 62
            },
            'BEA': {  # Oliver Bearman
                'skill': 75, 'consistency': 73, 'race_craft': 71, 'qualifying': 76,
                'wet_weather': 72, 'overtaking': 69, 'tire_management': 74,
                'pressure_handling': 70, 'championship_experience': 60
            }
        }
        
        # Team performance factors (2025 estimated)
        self.team_performance = {
            'Red Bull Racing Honda RBPT': {
                'car_performance': 92, 'strategy': 95, 'pit_stops': 98, 'reliability': 88
            },
            'McLaren Mercedes': {
                'car_performance': 95, 'strategy': 90, 'pit_stops': 92, 'reliability': 92
            },
            'Ferrari': {
                'car_performance': 89, 'strategy': 85, 'pit_stops': 88, 'reliability': 85
            },
            'Mercedes': {
                'car_performance': 87, 'strategy': 92, 'pit_stops': 95, 'reliability': 94
            },
            'Aston Martin Aramco Mercedes': {
                'car_performance': 82, 'strategy': 86, 'pit_stops': 85, 'reliability': 88
            },
            'Alpine Renault': {
                'car_performance': 78, 'strategy': 82, 'pit_stops': 83, 'reliability': 86
            },
            'Haas Ferrari': {
                'car_performance': 80, 'strategy': 78, 'pit_stops': 80, 'reliability': 84
            },
            'Racing Bulls Honda RBPT': {
                'car_performance': 79, 'strategy': 81, 'pit_stops': 85, 'reliability': 82
            },
            'Williams Mercedes': {
                'car_performance': 76, 'strategy': 79, 'pit_stops': 82, 'reliability': 81
            },
            'Kick Sauber Ferrari': {
                'car_performance': 74, 'strategy': 77, 'pit_stops': 78, 'reliability': 79
            }
        }
        
        # Enhanced track characteristics with more factors
        self.track_characteristics = {
            1: {  # Australia
                'power_sensitivity': 0.7, 'aero_sensitivity': 0.6, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.6, 'weather_variability': 0.4, 'track_evolution': 0.7,
                'safety_car_probability': 0.3, 'red_flag_probability': 0.1
            },
            2: {  # China
                'power_sensitivity': 0.8, 'aero_sensitivity': 0.7, 'tire_degradation': 0.7,
                'overtaking_difficulty': 0.4, 'weather_variability': 0.6, 'track_evolution': 0.6,
                'safety_car_probability': 0.2, 'red_flag_probability': 0.05
            },
            3: {  # Japan
                'power_sensitivity': 0.6, 'aero_sensitivity': 0.9, 'tire_degradation': 0.6,
                'overtaking_difficulty': 0.7, 'weather_variability': 0.7, 'track_evolution': 0.5,
                'safety_car_probability': 0.2, 'red_flag_probability': 0.1
            },
            4: {  # Bahrain
                'power_sensitivity': 0.8, 'aero_sensitivity': 0.6, 'tire_degradation': 0.9,
                'overtaking_difficulty': 0.3, 'weather_variability': 0.2, 'track_evolution': 0.8,
                'safety_car_probability': 0.15, 'red_flag_probability': 0.05
            },
            5: {  # Saudi Arabia
                'power_sensitivity': 0.9, 'aero_sensitivity': 0.5, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.8, 'weather_variability': 0.1, 'track_evolution': 0.6,
                'safety_car_probability': 0.4, 'red_flag_probability': 0.15
            },
            6: {  # Miami
                'power_sensitivity': 0.7, 'aero_sensitivity': 0.7, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.5, 'weather_variability': 0.6, 'track_evolution': 0.7,
                'safety_car_probability': 0.3, 'red_flag_probability': 0.1
            },
            7: {  # Imola
                'power_sensitivity': 0.6, 'aero_sensitivity': 0.8, 'tire_degradation': 0.7,
                'overtaking_difficulty': 0.8, 'weather_variability': 0.5, 'track_evolution': 0.6,
                'safety_car_probability': 0.25, 'red_flag_probability': 0.1
            },
            8: {  # Monaco
                'power_sensitivity': 0.3, 'aero_sensitivity': 0.9, 'tire_degradation': 0.5,
                'overtaking_difficulty': 0.95, 'weather_variability': 0.3, 'track_evolution': 0.9,
                'safety_car_probability': 0.6, 'red_flag_probability': 0.2
            },
            9: {  # Spain
                'power_sensitivity': 0.7, 'aero_sensitivity': 0.8, 'tire_degradation': 0.7,
                'overtaking_difficulty': 0.6, 'weather_variability': 0.4, 'track_evolution': 0.5,
                'safety_car_probability': 0.15, 'red_flag_probability': 0.05
            },
            10: {  # Canada
                'power_sensitivity': 0.8, 'aero_sensitivity': 0.6, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.4, 'weather_variability': 0.6, 'track_evolution': 0.7,
                'safety_car_probability': 0.35, 'red_flag_probability': 0.15
            },
            11: {  # Austria
                'power_sensitivity': 0.9, 'aero_sensitivity': 0.5, 'tire_degradation': 0.9,
                'overtaking_difficulty': 0.3, 'weather_variability': 0.6, 'track_evolution': 0.6,
                'safety_car_probability': 0.2, 'red_flag_probability': 0.08
            },
            12: {  # Britain
                'power_sensitivity': 0.8, 'aero_sensitivity': 0.7, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.4, 'weather_variability': 0.8, 'track_evolution': 0.6,
                'safety_car_probability': 0.25, 'red_flag_probability': 0.1
            },
            13: {  # Belgium
                'power_sensitivity': 0.9, 'aero_sensitivity': 0.6, 'tire_degradation': 0.6,
                'overtaking_difficulty': 0.3, 'weather_variability': 0.7, 'track_evolution': 0.5,
                'safety_car_probability': 0.3, 'red_flag_probability': 0.15
            },
            14: {  # Hungary
                'power_sensitivity': 0.5, 'aero_sensitivity': 0.9, 'tire_degradation': 0.9,
                'overtaking_difficulty': 0.9, 'weather_variability': 0.5, 'track_evolution': 0.8,
                'safety_car_probability': 0.2, 'red_flag_probability': 0.08
            },
            15: {  # Netherlands
                'power_sensitivity': 0.7, 'aero_sensitivity': 0.8, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.6, 'weather_variability': 0.6, 'track_evolution': 0.7,
                'safety_car_probability': 0.25, 'red_flag_probability': 0.1
            },
            16: {  # Italy
                'power_sensitivity': 0.9, 'aero_sensitivity': 0.4, 'tire_degradation': 0.7,
                'overtaking_difficulty': 0.2, 'weather_variability': 0.4, 'track_evolution': 0.5,
                'safety_car_probability': 0.2, 'red_flag_probability': 0.08
            },
            17: {  # Azerbaijan
                'power_sensitivity': 0.9, 'aero_sensitivity': 0.5, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.6, 'weather_variability': 0.3, 'track_evolution': 0.7,
                'safety_car_probability': 0.5, 'red_flag_probability': 0.2
            },
            18: {  # Singapore
                'power_sensitivity': 0.6, 'aero_sensitivity': 0.8, 'tire_degradation': 0.9,
                'overtaking_difficulty': 0.8, 'weather_variability': 0.6, 'track_evolution': 0.8,
                'safety_car_probability': 0.4, 'red_flag_probability': 0.15
            },
            19: {  # USA
                'power_sensitivity': 0.8, 'aero_sensitivity': 0.7, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.4, 'weather_variability': 0.5, 'track_evolution': 0.7,
                'safety_car_probability': 0.25, 'red_flag_probability': 0.1
            },
            20: {  # Mexico
                'power_sensitivity': 0.7, 'aero_sensitivity': 0.8, 'tire_degradation': 0.9,
                'overtaking_difficulty': 0.5, 'weather_variability': 0.4, 'track_evolution': 0.6,
                'safety_car_probability': 0.3, 'red_flag_probability': 0.12
            },
            21: {  # Brazil
                'power_sensitivity': 0.7, 'aero_sensitivity': 0.8, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.4, 'weather_variability': 0.8, 'track_evolution': 0.7,
                'safety_car_probability': 0.4, 'red_flag_probability': 0.2
            },
            22: {  # Las Vegas
                'power_sensitivity': 0.9, 'aero_sensitivity': 0.5, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.4, 'weather_variability': 0.2, 'track_evolution': 0.6,
                'safety_car_probability': 0.3, 'red_flag_probability': 0.1
            },
            23: {  # Qatar
                'power_sensitivity': 0.8, 'aero_sensitivity': 0.7, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.5, 'weather_variability': 0.2, 'track_evolution': 0.6,
                'safety_car_probability': 0.2, 'red_flag_probability': 0.08
            },
            24: {  # Abu Dhabi
                'power_sensitivity': 0.8, 'aero_sensitivity': 0.7, 'tire_degradation': 0.8,
                'overtaking_difficulty': 0.5, 'weather_variability': 0.2, 'track_evolution': 0.6,
                'safety_car_probability': 0.25, 'red_flag_probability': 0.1
            }
        }
        
        # Driver-team combinations with performance multipliers
        self.driver_team_synergy = {
            ('VER', 'Red Bull Racing Honda RBPT'): 1.05,
            ('LEC', 'Ferrari'): 1.03,
            ('HAM', 'Ferrari'): 0.98,  # New team, adjustment period
            ('RUS', 'Mercedes'): 1.02,
            ('NOR', 'McLaren Mercedes'): 1.04,
            ('PIA', 'McLaren Mercedes'): 1.01,
            ('ALO', 'Aston Martin Aramco Mercedes'): 1.03,
            # Add more combinations as needed
        }

    def get_historical_performance(self, driver, track_id, years_back=3):
        """Get historical performance for a driver at a specific track"""
        try:
            # This would ideally fetch real historical data
            # For now, simulate based on driver ratings and track characteristics
            driver_rating = self.driver_ratings.get(driver, {})
            track_char = self.track_characteristics.get(track_id, {})
            
            # Simulate historical performance based on driver strengths and track characteristics
            base_performance = driver_rating.get('skill', 75) / 100
            
            # Adjust for track characteristics
            if track_char.get('overtaking_difficulty', 0.5) > 0.7:
                # Qualifying becomes more important on overtaking-difficult tracks
                performance_adj = driver_rating.get('qualifying', 75) / 100
            else:
                # Race craft more important on overtaking-friendly tracks
                performance_adj = driver_rating.get('race_craft', 75) / 100
            
            # Add some randomness for realism
            historical_avg_position = max(1, min(20, 
                10 - (base_performance * performance_adj - 0.5) * 15 + np.random.normal(0, 2)
            ))
            
            return {
                'avg_position': historical_avg_position,
                'avg_grid': historical_avg_position + np.random.normal(0, 1.5),
                'podiums': max(0, int((1 - historical_avg_position/20) * years_back * 2)),
                'wins': max(0, int((1 - historical_avg_position/20) * years_back * 0.5))
            }
            
        except Exception as e:
            self.logger.error(f"Error getting historical performance: {str(e)}")
            return {'avg_position': 10, 'avg_grid': 10, 'podiums': 0, 'wins': 0}

    def calculate_dynamic_factors(self, year, round_num):
        """Calculate dynamic factors that affect race outcome"""
        factors = {}
        
        # Season progression factor
        factors['season_progress'] = round_num / 24
        
        # Championship pressure (simulate based on round)
        if round_num > 15:  # Late season
            factors['championship_pressure'] = 1.2
        elif round_num > 10:  # Mid season
            factors['championship_pressure'] = 1.0
        else:  # Early season
            factors['championship_pressure'] = 0.8
        
        # Simulated weather probability
        track_char = self.track_characteristics.get(round_num, {})
        weather_var = track_char.get('weather_variability', 0.5)
        
        if np.random.random() < weather_var * 0.3:  # 30% chance of challenging weather
            if np.random.random() < 0.7:
                factors['weather_condition'] = 'wet'
            else:
                factors['weather_condition'] = 'mixed'
        else:
            factors['weather_condition'] = 'dry'
        
        # Safety car probability
        factors['safety_car_probability'] = track_char.get('safety_car_probability', 0.25)
        
        return factors

    def build_feature_matrix(self, drivers, year, round_num):
        """Build comprehensive feature matrix for ML prediction"""
        features = []
        driver_names = []
        
        track_char = self.track_characteristics.get(round_num, {})
        dynamic_factors = self.calculate_dynamic_factors(year, round_num)
        
        for driver in drivers:
            driver_rating = self.driver_ratings.get(driver, {})
            historical = self.get_historical_performance(driver, round_num)
            
            # Get team performance (need to map driver to team)
            team = self.get_driver_team(driver)
            team_perf = self.team_performance.get(team, {})
            
            # Calculate synergy multiplier
            synergy = self.driver_team_synergy.get((driver, team), 1.0)
            
            feature_vector = [
                # Driver characteristics
                driver_rating.get('skill', 75) / 100,
                driver_rating.get('consistency', 75) / 100,
                driver_rating.get('race_craft', 75) / 100,
                driver_rating.get('qualifying', 75) / 100,
                driver_rating.get('wet_weather', 75) / 100,
                driver_rating.get('overtaking', 75) / 100,
                driver_rating.get('tire_management', 75) / 100,
                driver_rating.get('pressure_handling', 75) / 100,
                driver_rating.get('championship_experience', 75) / 100,
                
                # Team characteristics
                team_perf.get('car_performance', 75) / 100,
                team_perf.get('strategy', 75) / 100,
                team_perf.get('pit_stops', 75) / 100,
                team_perf.get('reliability', 75) / 100,
                
                # Track characteristics
                track_char.get('power_sensitivity', 0.5),
                track_char.get('aero_sensitivity', 0.5),
                track_char.get('tire_degradation', 0.5),
                track_char.get('overtaking_difficulty', 0.5),
                track_char.get('weather_variability', 0.5),
                track_char.get('track_evolution', 0.5),
                track_char.get('safety_car_probability', 0.25),
                
                # Historical performance
                min(historical['avg_position'] / 20, 1.0),
                min(historical['avg_grid'] / 20, 1.0),
                min(historical['podiums'] / 10, 1.0),
                min(historical['wins'] / 5, 1.0),
                
                # Dynamic factors
                dynamic_factors['season_progress'],
                dynamic_factors['championship_pressure'],
                1.0 if dynamic_factors['weather_condition'] == 'wet' else 0.0,
                1.0 if dynamic_factors['weather_condition'] == 'mixed' else 0.0,
                
                # Synergy factor
                synergy
            ]
            
            features.append(feature_vector)
            driver_names.append(driver)
        
        return np.array(features), driver_names, dynamic_factors

    def get_driver_team(self, driver):
        """Map driver to current team (2025)"""
        driver_team_mapping = {
            'VER': 'Red Bull Racing Honda RBPT',
            'LAW': 'Red Bull Racing Honda RBPT',
            'LEC': 'Ferrari',
            'HAM': 'Ferrari',
            'RUS': 'Mercedes',
            'ANT': 'Mercedes',  # Antonelli
            'NOR': 'McLaren Mercedes',
            'PIA': 'McLaren Mercedes',
            'ALO': 'Aston Martin Aramco Mercedes',
            'STR': 'Aston Martin Aramco Mercedes',
            'GAS': 'Alpine Renault',
            'DOO': 'Alpine Renault',
            'HUL': 'Haas Ferrari',
            'OCO': 'Haas Ferrari',
            'ALB': 'Williams Mercedes',
            'SAI': 'Williams Mercedes',
            'TSU': 'Racing Bulls Honda RBPT',
            'HAD': 'Racing Bulls Honda RBPT',  # Hadjar
            'COL': 'Kick Sauber Ferrari',  # Colapinto
            'BEA': 'Kick Sauber Ferrari'   # Bearman
        }
        return driver_team_mapping.get(driver, 'Unknown Team')

    def train_models(self, training_data=None):
        """Train ML models for race prediction"""
        try:
            if training_data is None:
                # Generate synthetic training data based on ratings and historical patterns
                training_data = self._generate_training_data()
            
            X, y_position, y_win_prob, y_podium_prob, y_points_prob = training_data
            
            # Train position prediction model
            self.position_model = GradientBoostingRegressor(
                n_estimators=100, learning_rate=0.1, max_depth=6, random_state=42
            )
            self.position_model.fit(X, y_position)
            
            # Train probability models
            self.win_probability_model = RandomForestRegressor(
                n_estimators=100, max_depth=8, random_state=42
            )
            self.win_probability_model.fit(X, y_win_prob)
            
            self.podium_probability_model = RandomForestRegressor(
                n_estimators=100, max_depth=8, random_state=42
            )
            self.podium_probability_model.fit(X, y_podium_prob)
            
            self.points_probability_model = RandomForestRegressor(
                n_estimators=100, max_depth=8, random_state=42
            )
            self.points_probability_model.fit(X, y_points_prob)
            
            # Fit scaler
            self.scaler.fit(X)
            
            self.logger.info("ML models trained successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error training models: {str(e)}")
            return False

    def _generate_training_data(self, n_samples=5000):
        """Generate synthetic training data based on driver/team ratings"""
        X = []
        y_position = []
        y_win_prob = []
        y_podium_prob = []
        y_points_prob = []
        
        all_drivers = list(self.driver_ratings.keys())  # All available drivers
        
        for _ in range(n_samples):
            # Random track and season parameters
            track_id = np.random.randint(1, 25)
            round_num = np.random.randint(1, 25)
            
            # Select drivers (ensure we don't try to sample more than available)
            max_drivers = len(all_drivers)
            num_drivers = min(20, max_drivers)
            
            # Sometimes use fewer drivers for variety
            if np.random.random() < 0.2 and num_drivers > 15:
                num_drivers = max(15, num_drivers - np.random.randint(1, 6))
            
            try:
                race_drivers = np.random.choice(all_drivers, size=num_drivers, replace=False)
                features, _, _ = self.build_feature_matrix(race_drivers, 2024, round_num)
                
                # Simulate race outcomes based on features
                for i, feature_vector in enumerate(features):
                    # Calculate expected position based on overall performance
                    overall_performance = np.mean(feature_vector[:13])  # Driver + team features
                    track_suitability = np.mean(feature_vector[13:21])  # Track features
                    
                    # Add randomness for realistic variance
                    performance_score = overall_performance * track_suitability
                    noise = np.random.normal(0, 0.15)
                    final_score = performance_score + noise
                    
                    # Convert to position (1-num_drivers)
                    position = max(1, min(num_drivers, int(num_drivers + 1 - final_score * num_drivers)))
                    
                    # Calculate probabilities
                    win_prob = max(0, min(1, (num_drivers + 1 - position) / num_drivers * 0.8 + np.random.normal(0, 0.1)))
                    podium_prob = max(0, min(1, (num_drivers + 1 - position) / num_drivers * 0.6 + np.random.normal(0, 0.15)))
                    points_prob = max(0, min(1, (num_drivers + 1 - position) / num_drivers * 0.4 + np.random.normal(0, 0.2)))
                    
                    X.append(feature_vector)
                    y_position.append(position)
                    y_win_prob.append(win_prob)
                    y_podium_prob.append(podium_prob)
                    y_points_prob.append(points_prob)
                    
            except Exception as e:
                # Skip this iteration if there's an error
                self.logger.warning(f"Skipping training sample due to error: {str(e)}")
                continue
        
        # Ensure we have enough training data
        if len(X) < 100:  # Minimum required for training
            self.logger.warning(f"Only generated {len(X)} training samples, creating additional synthetic data")
            
            # Create basic training data using just the first few drivers
            basic_drivers = list(self.driver_ratings.keys())[:10]
            for i in range(100 - len(X)):
                try:
                    # Use fewer drivers for basic training
                    sample_drivers = np.random.choice(basic_drivers, size=min(10, len(basic_drivers)), replace=False)
                    features, _, _ = self.build_feature_matrix(sample_drivers, 2024, 1)
                    
                    for j, feature_vector in enumerate(features):
                        position = j + 1  # Simple position assignment
                        win_prob = 1.0 / (position + 1)
                        podium_prob = 1.0 / max(1, position - 1)
                        points_prob = 1.0 if position <= 10 else 0.0
                        
                        X.append(feature_vector)
                        y_position.append(position)
                        y_win_prob.append(win_prob)
                        y_podium_prob.append(podium_prob)
                        y_points_prob.append(points_prob)
                        
                        if len(X) >= 100:
                            break
                    
                    if len(X) >= 100:
                        break
                        
                except Exception as e2:
                    self.logger.warning(f"Error creating basic training data: {str(e2)}")
                    continue
        
        return np.array(X), np.array(y_position), np.array(y_win_prob), np.array(y_podium_prob), np.array(y_points_prob)

    def predict_race_outcome(self, year, round_num):
        """Enhanced race outcome prediction"""
        try:
            # Active drivers for 2025
            active_drivers = [
                'VER', 'LAW', 'LEC', 'HAM', 'RUS', 'ANT', 'NOR', 'PIA',
                'ALO', 'STR', 'GAS', 'DOO', 'HUL', 'OCO', 'ALB', 'SAI',
                'TSU', 'HAD', 'COL', 'BEA'
            ]
            
            # Train models if not already trained
            if self.position_model is None:
                self.logger.info("Training ML models...")
                if not self.train_models():
                    return self._generate_fallback_predictions(year, round_num)
            
            # Build feature matrix
            features, driver_names, dynamic_factors = self.build_feature_matrix(
                active_drivers, year, round_num
            )
            
            # Scale features
            features_scaled = self.scaler.transform(features)
            
            # Make predictions
            predicted_positions = self.position_model.predict(features_scaled)
            win_probabilities = self.win_probability_model.predict(features_scaled)
            podium_probabilities = self.podium_probability_model.predict(features_scaled)
            points_probabilities = self.points_probability_model.predict(features_scaled)
            
            # Ensure probabilities are valid
            win_probabilities = np.clip(win_probabilities, 0, 1)
            podium_probabilities = np.clip(podium_probabilities, 0, 1)
            points_probabilities = np.clip(points_probabilities, 0, 1)
            
            # Create prediction results
            predictions = []
            for i, driver in enumerate(driver_names):
                predictions.append({
                    'driver': driver,
                    'predicted_position': float(predicted_positions[i]),
                    'win_probability': float(win_probabilities[i]),
                    'podium_probability': float(podium_probabilities[i]),
                    'points_probability': float(points_probabilities[i])
                })
            
            # Sort by predicted position for final results
            predictions.sort(key=lambda x: x['predicted_position'])
            
            # Get race info
            race_info = self._get_race_info(year, round_num)
            
            # Format results
            winner_prediction = max(predictions, key=lambda x: x['win_probability'])
            
            podium_predictions = sorted(predictions, key=lambda x: x['podium_probability'], reverse=True)[:8]
            points_predictions = sorted(predictions, key=lambda x: x['points_probability'], reverse=True)[:10]
            
            return {
                'race_info': race_info,
                'winner_prediction': {
                    'driver': winner_prediction['driver'],
                    'probability': winner_prediction['win_probability']
                },
                'podium_predictions': [
                    {'driver': p['driver'], 'probability': p['podium_probability']} 
                    for p in podium_predictions
                ],
                'points_predictions': [
                    {'driver': p['driver'], 'probability': p['points_probability']} 
                    for p in points_predictions
                ],
                'full_predictions': predictions,
                'dynamic_factors': dynamic_factors,
                'model_confidence': self._calculate_model_confidence(predictions)
            }
            
        except Exception as e:
            self.logger.error(f"Error in enhanced race prediction: {str(e)}")
            return self._generate_fallback_predictions(year, round_num)

    def _calculate_model_confidence(self, predictions):
        """Calculate overall model confidence based on prediction variance"""
        win_probs = [p['win_probability'] for p in predictions]
        variance = np.var(win_probs)
        
        # Higher variance = lower confidence (more uncertainty)
        # Scale to 0-1 where 1 is high confidence
        confidence = max(0, min(1, 1 - variance * 4))
        return confidence

    def _get_race_info(self, year, round_num):
        """Get race information"""
        race_names = {
            1: 'Australian Grand Prix', 2: 'Chinese Grand Prix', 3: 'Japanese Grand Prix',
            4: 'Bahrain Grand Prix', 5: 'Saudi Arabian Grand Prix', 6: 'Miami Grand Prix',
            7: 'Emilia Romagna Grand Prix', 8: 'Monaco Grand Prix', 9: 'Spanish Grand Prix',
            10: 'Canadian Grand Prix', 11: 'Austrian Grand Prix', 12: 'British Grand Prix',
            13: 'Belgian Grand Prix', 14: 'Hungarian Grand Prix', 15: 'Dutch Grand Prix',
            16: 'Italian Grand Prix', 17: 'Azerbaijan Grand Prix', 18: 'Singapore Grand Prix',
            19: 'United States Grand Prix', 20: 'Mexico City Grand Prix', 21: 'São Paulo Grand Prix',
            22: 'Las Vegas Grand Prix', 23: 'Qatar Grand Prix', 24: 'Abu Dhabi Grand Prix'
        }
        
        circuits = {
            1: 'Albert Park Circuit', 2: 'Shanghai International Circuit', 3: 'Suzuka Circuit',
            4: 'Bahrain International Circuit', 5: 'Jeddah Corniche Circuit',
            6: 'Miami International Autodrome', 7: 'Autodromo Enzo e Dino Ferrari',
            8: 'Circuit de Monaco', 9: 'Circuit de Barcelona-Catalunya',
            10: 'Circuit Gilles Villeneuve', 11: 'Red Bull Ring', 12: 'Silverstone Circuit',
            13: 'Circuit de Spa-Francorchamps', 14: 'Hungaroring', 15: 'Circuit Zandvoort',
            16: 'Autodromo Nazionale di Monza', 17: 'Baku City Circuit',
            18: 'Marina Bay Street Circuit', 19: 'Circuit of the Americas',
            20: 'Autódromo Hermanos Rodríguez', 21: 'Interlagos',
            22: 'Las Vegas Strip Street Circuit', 23: 'Lusail International Circuit',
            24: 'Yas Marina Circuit'
        }
        
        return {
            'round': round_num,
            'race_name': race_names.get(round_num, f'Race {round_num}'),
            'circuit': circuits.get(round_num, 'Unknown Circuit'),
            'date': f'2025-{3 + (round_num-1)//4:02d}-{1 + (round_num-1)*7%28:02d}'
        }

    def _generate_fallback_predictions(self, year, round_num):
        """Generate fallback predictions when ML models fail"""
        return {
            'race_info': self._get_race_info(year, round_num),
            'winner_prediction': {'driver': 'VER', 'probability': 0.25},
            'podium_predictions': [
                {'driver': 'VER', 'probability': 0.25},
                {'driver': 'LEC', 'probability': 0.20},
                {'driver': 'HAM', 'probability': 0.18},
                {'driver': 'RUS', 'probability': 0.15},
                {'driver': 'NOR', 'probability': 0.14},
                {'driver': 'PIA', 'probability': 0.12},
                {'driver': 'ALO', 'probability': 0.10},
                {'driver': 'SAI', 'probability': 0.08}
            ],
            'points_predictions': [
                {'driver': 'VER', 'probability': 0.90},
                {'driver': 'LEC', 'probability': 0.85},
                {'driver': 'HAM', 'probability': 0.80},
                {'driver': 'RUS', 'probability': 0.75},
                {'driver': 'NOR', 'probability': 0.70},
                {'driver': 'PIA', 'probability': 0.65},
                {'driver': 'ALO', 'probability': 0.60},
                {'driver': 'SAI', 'probability': 0.55},
                {'driver': 'STR', 'probability': 0.35},
                {'driver': 'ALB', 'probability': 0.30}
            ],
            'model_confidence': 0.6,
            'dynamic_factors': {'weather_condition': 'dry', 'championship_pressure': 1.0}
        }

# Create an alias for backward compatibility
class RacePredictor(EnhancedRacePredictor):
    """Backward compatibility alias"""
    pass 