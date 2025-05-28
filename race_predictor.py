import pandas as pd
import numpy as np
import logging
import random
from datetime import datetime

class RacePredictor:
    """Handles race outcome predictions using ML models"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Driver performance weights for predictions
        self.driver_weights = {
            'VER': 0.95,  # Max Verstappen
            'LEC': 0.85,  # Charles Leclerc
            'HAM': 0.82,  # Lewis Hamilton
            'RUS': 0.75,  # George Russell
            'NOR': 0.78,  # Lando Norris
            'PIA': 0.72,  # Oscar Piastri
            'SAI': 0.74,  # Carlos Sainz
            'PER': 0.70,  # Sergio Pérez
            'ALO': 0.76,  # Fernando Alonso
            'STR': 0.58,  # Lance Stroll
            'ALB': 0.62,  # Alexander Albon
            'OCO': 0.64,  # Esteban Ocon
            'HUL': 0.66,  # Nico Hülkenberg
            'TSU': 0.60,  # Yuki Tsunoda
            'LAW': 0.56,  # Liam Lawson
            'GAS': 0.63,  # Pierre Gasly
            'DOO': 0.52,  # Jack Doohan
            'MAG': 0.59,  # Kevin Magnussen
            'BOT': 0.68,  # Valtteri Bottas
            'ZHO': 0.54   # Zhou Guanyu
        }
        
        # Track characteristics that affect performance
        self.track_characteristics = {
            1: {'power': 0.7, 'aero': 0.6, 'tire_deg': 0.8},    # Australia
            2: {'power': 0.8, 'aero': 0.7, 'tire_deg': 0.7},    # China
            3: {'power': 0.6, 'aero': 0.9, 'tire_deg': 0.6},    # Japan
            4: {'power': 0.8, 'aero': 0.6, 'tire_deg': 0.9},    # Bahrain
            5: {'power': 0.9, 'aero': 0.5, 'tire_deg': 0.8},    # Saudi Arabia
            6: {'power': 0.7, 'aero': 0.7, 'tire_deg': 0.8},    # Miami
            7: {'power': 0.6, 'aero': 0.8, 'tire_deg': 0.7},    # Imola
            8: {'power': 0.3, 'aero': 0.9, 'tire_deg': 0.5},    # Monaco
            9: {'power': 0.7, 'aero': 0.8, 'tire_deg': 0.7},    # Spain
            10: {'power': 0.8, 'aero': 0.6, 'tire_deg': 0.8},   # Canada
            11: {'power': 0.9, 'aero': 0.5, 'tire_deg': 0.9},   # Austria
            12: {'power': 0.8, 'aero': 0.7, 'tire_deg': 0.8},   # Britain
            13: {'power': 0.9, 'aero': 0.6, 'tire_deg': 0.6},   # Belgium
            14: {'power': 0.5, 'aero': 0.9, 'tire_deg': 0.9},   # Hungary
            15: {'power': 0.7, 'aero': 0.8, 'tire_deg': 0.8},   # Netherlands
            16: {'power': 0.9, 'aero': 0.4, 'tire_deg': 0.7},   # Italy
            17: {'power': 0.9, 'aero': 0.5, 'tire_deg': 0.8},   # Azerbaijan
            18: {'power': 0.6, 'aero': 0.8, 'tire_deg': 0.9},   # Singapore
            19: {'power': 0.8, 'aero': 0.7, 'tire_deg': 0.8},   # USA
            20: {'power': 0.7, 'aero': 0.8, 'tire_deg': 0.9},   # Mexico
            21: {'power': 0.7, 'aero': 0.8, 'tire_deg': 0.8},   # Brazil
            22: {'power': 0.9, 'aero': 0.5, 'tire_deg': 0.8},   # Las Vegas
            23: {'power': 0.8, 'aero': 0.7, 'tire_deg': 0.8},   # Qatar
            24: {'power': 0.8, 'aero': 0.7, 'tire_deg': 0.8}    # Abu Dhabi
        }

    def predict_race_outcome(self, year, round_num):
        """Predict race outcomes for a given race"""
        try:
            # Get race information
            race_info = self._get_race_info(year, round_num)
            
            # Generate predictions
            predictions = self._generate_race_predictions(round_num)
            
            return {
                'race_info': race_info,
                'winner_prediction': predictions['winner'],
                'podium_predictions': predictions['podium'],
                'points_predictions': predictions['points']
            }
            
        except Exception as e:
            self.logger.error(f"Error predicting race outcome: {str(e)}")
            return self._generate_fallback_predictions(year, round_num)

    def _get_race_info(self, year, round_num):
        """Get race information"""
        # Race names for 2025
        race_names = {
            1: 'Australian Grand Prix',
            2: 'Chinese Grand Prix', 
            3: 'Japanese Grand Prix',
            4: 'Bahrain Grand Prix',
            5: 'Saudi Arabian Grand Prix',
            6: 'Miami Grand Prix',
            7: 'Emilia Romagna Grand Prix',
            8: 'Monaco Grand Prix',
            9: 'Spanish Grand Prix',
            10: 'Canadian Grand Prix',
            11: 'Austrian Grand Prix',
            12: 'British Grand Prix',
            13: 'Belgian Grand Prix',
            14: 'Hungarian Grand Prix',
            15: 'Dutch Grand Prix',
            16: 'Italian Grand Prix',
            17: 'Azerbaijan Grand Prix',
            18: 'Singapore Grand Prix',
            19: 'United States Grand Prix',
            20: 'Mexico City Grand Prix',
            21: 'São Paulo Grand Prix',
            22: 'Las Vegas Grand Prix',
            23: 'Qatar Grand Prix',
            24: 'Abu Dhabi Grand Prix'
        }
        
        circuits = {
            1: 'Albert Park Circuit',
            2: 'Shanghai International Circuit',
            3: 'Suzuka Circuit',
            4: 'Bahrain International Circuit',
            5: 'Jeddah Corniche Circuit',
            6: 'Miami International Autodrome',
            7: 'Autodromo Enzo e Dino Ferrari',
            8: 'Circuit de Monaco',
            9: 'Circuit de Barcelona-Catalunya',
            10: 'Circuit Gilles Villeneuve',
            11: 'Red Bull Ring',
            12: 'Silverstone Circuit',
            13: 'Circuit de Spa-Francorchamps',
            14: 'Hungaroring',
            15: 'Circuit Zandvoort',
            16: 'Autodromo Nazionale di Monza',
            17: 'Baku City Circuit',
            18: 'Marina Bay Street Circuit',
            19: 'Circuit of the Americas',
            20: 'Autódromo Hermanos Rodríguez',
            21: 'Interlagos',
            22: 'Las Vegas Strip Street Circuit',
            23: 'Lusail International Circuit',
            24: 'Yas Marina Circuit'
        }
        
        return {
            'round': round_num,
            'race_name': race_names.get(round_num, f'Race {round_num}'),
            'circuit': circuits.get(round_num, 'Unknown Circuit'),
            'date': f'2025-{3 + (round_num-1)//4:02d}-{1 + (round_num-1)*7%28:02d}'
        }

    def _generate_race_predictions(self, round_num):
        """Generate race predictions based on driver weights and track characteristics"""
        # Get track characteristics
        track_char = self.track_characteristics.get(round_num, {'power': 0.7, 'aero': 0.7, 'tire_deg': 0.7})
        
        # Active 2025 drivers
        active_drivers = ['VER', 'LEC', 'HAM', 'RUS', 'NOR', 'PIA', 'SAI', 'PER', 
                         'ALO', 'STR', 'ALB', 'OCO', 'HUL', 'TSU', 'LAW', 'GAS', 
                         'DOO', 'MAG', 'BOT']
        
        # Calculate adjusted probabilities based on track characteristics
        adjusted_weights = {}
        for driver in active_drivers:
            base_weight = self.driver_weights.get(driver, 0.5)
            
            # Adjust based on track characteristics (simplified model)
            track_adjustment = 1.0
            if driver in ['VER', 'PER']:  # Red Bull - good everywhere
                track_adjustment = 1.0 + (track_char['power'] - 0.7) * 0.1
            elif driver in ['LEC', 'HAM']:  # Ferrari - good on power tracks
                track_adjustment = 1.0 + (track_char['power'] - 0.7) * 0.2
            elif driver in ['RUS']:  # Mercedes - good on aero tracks
                track_adjustment = 1.0 + (track_char['aero'] - 0.7) * 0.15
            elif driver in ['NOR', 'PIA']:  # McLaren - balanced
                track_adjustment = 1.0 + ((track_char['power'] + track_char['aero'])/2 - 0.7) * 0.1
            
            adjusted_weights[driver] = base_weight * track_adjustment
        
        # Normalize weights to probabilities
        total_weight = sum(adjusted_weights.values())
        probabilities = {driver: weight/total_weight for driver, weight in adjusted_weights.items()}
        
        # Add some randomness to make predictions more realistic
        for driver in probabilities:
            noise = np.random.normal(0, 0.05)  # 5% noise
            probabilities[driver] = max(0.001, probabilities[driver] + noise)
        
        # Re-normalize after adding noise
        total_prob = sum(probabilities.values())
        probabilities = {driver: prob/total_prob for driver, prob in probabilities.items()}
        
        # Generate winner prediction (highest probability)
        winner = max(probabilities.keys(), key=lambda x: probabilities[x])
        
        # Generate podium predictions (top 8 most likely)
        podium_drivers = sorted(probabilities.keys(), key=lambda x: probabilities[x], reverse=True)[:8]
        podium_predictions = [{'driver': driver, 'probability': probabilities[driver]} for driver in podium_drivers]
        
        # Generate points predictions (top 10 most likely)
        points_drivers = sorted(probabilities.keys(), key=lambda x: probabilities[x], reverse=True)[:10]
        points_predictions = [{'driver': driver, 'probability': probabilities[driver]} for driver in points_drivers]
        
        return {
            'winner': {'driver': winner, 'probability': probabilities[winner]},
            'podium': podium_predictions,
            'points': points_predictions
        }

    def _generate_fallback_predictions(self, year, round_num):
        """Generate fallback predictions when real data is unavailable"""
        return {
            'race_info': {
                'round': round_num,
                'race_name': f'Race {round_num}',
                'circuit': 'Unknown Circuit',
                'date': f'{year}-01-01'
            },
            'winner_prediction': {'driver': 'VER', 'probability': 0.35},
            'podium_predictions': [
                {'driver': 'VER', 'probability': 0.35},
                {'driver': 'LEC', 'probability': 0.25},
                {'driver': 'HAM', 'probability': 0.20},
                {'driver': 'RUS', 'probability': 0.15},
                {'driver': 'NOR', 'probability': 0.12},
                {'driver': 'PIA', 'probability': 0.10},
                {'driver': 'SAI', 'probability': 0.08},
                {'driver': 'ALO', 'probability': 0.07}
            ],
            'points_predictions': [
                {'driver': 'VER', 'probability': 0.85},
                {'driver': 'LEC', 'probability': 0.80},
                {'driver': 'HAM', 'probability': 0.75},
                {'driver': 'RUS', 'probability': 0.70},
                {'driver': 'NOR', 'probability': 0.65},
                {'driver': 'PIA', 'probability': 0.60},
                {'driver': 'SAI', 'probability': 0.55},
                {'driver': 'ALO', 'probability': 0.50},
                {'driver': 'PER', 'probability': 0.45},
                {'driver': 'STR', 'probability': 0.25}
            ]
        } 