import fastf1
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Enable FastF1 cache
fastf1.Cache.enable_cache('cache')

class DataProcessor:
    """Handles F1 data processing and race information"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 2025 F1 Calendar (projected)
        self.races_2025 = [
            {'round': 1, 'name': 'Australian Grand Prix', 'location': 'Melbourne', 'country': 'Australia', 'circuit': 'Albert Park Circuit', 'date': '2025-03-16'},
            {'round': 2, 'name': 'Chinese Grand Prix', 'location': 'Shanghai', 'country': 'China', 'circuit': 'Shanghai International Circuit', 'date': '2025-03-23'},
            {'round': 3, 'name': 'Japanese Grand Prix', 'location': 'Suzuka', 'country': 'Japan', 'circuit': 'Suzuka Circuit', 'date': '2025-04-06'},
            {'round': 4, 'name': 'Bahrain Grand Prix', 'location': 'Sakhir', 'country': 'Bahrain', 'circuit': 'Bahrain International Circuit', 'date': '2025-04-13'},
            {'round': 5, 'name': 'Saudi Arabian Grand Prix', 'location': 'Jeddah', 'country': 'Saudi Arabia', 'circuit': 'Jeddah Corniche Circuit', 'date': '2025-04-20'},
            {'round': 6, 'name': 'Miami Grand Prix', 'location': 'Miami', 'country': 'USA', 'circuit': 'Miami International Autodrome', 'date': '2025-05-04'},
            {'round': 7, 'name': 'Emilia Romagna Grand Prix', 'location': 'Imola', 'country': 'Italy', 'circuit': 'Autodromo Enzo e Dino Ferrari', 'date': '2025-05-18'},
            {'round': 8, 'name': 'Monaco Grand Prix', 'location': 'Monte Carlo', 'country': 'Monaco', 'circuit': 'Circuit de Monaco', 'date': '2025-05-25'},
            {'round': 9, 'name': 'Spanish Grand Prix', 'location': 'Barcelona', 'country': 'Spain', 'circuit': 'Circuit de Barcelona-Catalunya', 'date': '2025-06-01'},
            {'round': 10, 'name': 'Canadian Grand Prix', 'location': 'Montreal', 'country': 'Canada', 'circuit': 'Circuit Gilles Villeneuve', 'date': '2025-06-15'},
            {'round': 11, 'name': 'Austrian Grand Prix', 'location': 'Spielberg', 'country': 'Austria', 'circuit': 'Red Bull Ring', 'date': '2025-06-29'},
            {'round': 12, 'name': 'British Grand Prix', 'location': 'Silverstone', 'country': 'United Kingdom', 'circuit': 'Silverstone Circuit', 'date': '2025-07-06'},
            {'round': 13, 'name': 'Belgian Grand Prix', 'location': 'Spa-Francorchamps', 'country': 'Belgium', 'circuit': 'Circuit de Spa-Francorchamps', 'date': '2025-07-27'},
            {'round': 14, 'name': 'Hungarian Grand Prix', 'location': 'Budapest', 'country': 'Hungary', 'circuit': 'Hungaroring', 'date': '2025-08-03'},
            {'round': 15, 'name': 'Dutch Grand Prix', 'location': 'Zandvoort', 'country': 'Netherlands', 'circuit': 'Circuit Zandvoort', 'date': '2025-08-31'},
            {'round': 16, 'name': 'Italian Grand Prix', 'location': 'Monza', 'country': 'Italy', 'circuit': 'Autodromo Nazionale di Monza', 'date': '2025-09-07'},
            {'round': 17, 'name': 'Azerbaijan Grand Prix', 'location': 'Baku', 'country': 'Azerbaijan', 'circuit': 'Baku City Circuit', 'date': '2025-09-21'},
            {'round': 18, 'name': 'Singapore Grand Prix', 'location': 'Singapore', 'country': 'Singapore', 'circuit': 'Marina Bay Street Circuit', 'date': '2025-10-05'},
            {'round': 19, 'name': 'United States Grand Prix', 'location': 'Austin', 'country': 'USA', 'circuit': 'Circuit of the Americas', 'date': '2025-10-19'},
            {'round': 20, 'name': 'Mexico City Grand Prix', 'location': 'Mexico City', 'country': 'Mexico', 'circuit': 'Autódromo Hermanos Rodríguez', 'date': '2025-10-26'},
            {'round': 21, 'name': 'São Paulo Grand Prix', 'location': 'São Paulo', 'country': 'Brazil', 'circuit': 'Interlagos', 'date': '2025-11-09'},
            {'round': 22, 'name': 'Las Vegas Grand Prix', 'location': 'Las Vegas', 'country': 'USA', 'circuit': 'Las Vegas Strip Street Circuit', 'date': '2025-11-22'},
            {'round': 23, 'name': 'Qatar Grand Prix', 'location': 'Lusail', 'country': 'Qatar', 'circuit': 'Lusail International Circuit', 'date': '2025-11-30'},
            {'round': 24, 'name': 'Abu Dhabi Grand Prix', 'location': 'Abu Dhabi', 'country': 'UAE', 'circuit': 'Yas Marina Circuit', 'date': '2025-12-07'}
        ]

    def get_season_races(self, year):
        """Get race calendar for a given year"""
        try:
            if year == 2025:
                return self.races_2025
            
            # For historical years, try to get from FastF1
            schedule = fastf1.get_event_schedule(year)
            if schedule.empty:
                self.logger.warning(f"No schedule found for {year}")
                return []
            
            races = []
            for idx, event in schedule.iterrows():
                if event['EventFormat'] == 'conventional':  # Only full race weekends
                    race_data = {
                        'round': event['RoundNumber'],
                        'name': event['EventName'],
                        'location': event['Location'],
                        'country': event['Country'],
                        'circuit': event['EventName'],  # Fallback
                        'date': event['EventDate'].strftime('%Y-%m-%d') if pd.notna(event['EventDate']) else 'TBD'
                    }
                    races.append(race_data)
            
            return races
            
        except Exception as e:
            self.logger.error(f"Error getting season races for {year}: {str(e)}")
            # Return fallback data
            if year == 2025:
                return self.races_2025
            return []

    def get_race_data(self, year, round_num):
        """Get detailed race data"""
        try:
            session = fastf1.get_session(year, round_num, 'R')
            session.load()
            
            # Get race results
            results = session.results
            if results.empty:
                return {'error': f'No results available for {year} Round {round_num}'}
            
            # Process results
            race_results = []
            for idx, result in results.iterrows():
                driver_result = {
                    'position': result.get('Position', 'DNF'),
                    'driver': result.get('Abbreviation', 'N/A'),
                    'driver_name': result.get('FullName', 'N/A'),
                    'team': result.get('TeamName', 'N/A'),
                    'grid_position': result.get('GridPosition', 'N/A'),
                    'points': result.get('Points', 0),
                    'time': str(result.get('Time', 'N/A')),
                    'status': result.get('Status', 'N/A')
                }
                race_results.append(driver_result)
            
            return {
                'race_info': {
                    'year': year,
                    'round': round_num,
                    'name': session.event['EventName'],
                    'date': session.event['EventDate'].strftime('%Y-%m-%d')
                },
                'results': race_results
            }
            
        except Exception as e:
            self.logger.error(f"Error getting race data: {str(e)}")
            return {'error': f'Unable to load race data for {year} Round {round_num}'}

    def get_season_standings(self, year):
        """Get championship standings for a season"""
        try:
            # For 2025, return mock data
            if year == 2025:
                return self._get_mock_standings_2025()
            
            # For historical years, try to calculate from race results
            return self._calculate_historical_standings(year)
            
        except Exception as e:
            self.logger.error(f"Error getting season standings: {str(e)}")
            return {'drivers': [], 'constructors': []}

    def _get_mock_standings_2025(self):
        """Mock standings for 2025 season"""
        mock_drivers = [
            {'driver': 'VER', 'name': 'Max Verstappen', 'team': 'Red Bull Racing', 'points': 575},
            {'driver': 'LEC', 'name': 'Charles Leclerc', 'team': 'Ferrari', 'points': 445},
            {'driver': 'NOR', 'name': 'Lando Norris', 'team': 'McLaren', 'points': 420},
            {'driver': 'HAM', 'name': 'Lewis Hamilton', 'team': 'Ferrari', 'points': 385},
            {'driver': 'PIA', 'name': 'Oscar Piastri', 'team': 'McLaren', 'points': 360},
            {'driver': 'RUS', 'name': 'George Russell', 'team': 'Mercedes', 'points': 340},
            {'driver': 'SAI', 'name': 'Carlos Sainz', 'team': 'Williams', 'points': 285},
            {'driver': 'PER', 'name': 'Sergio Pérez', 'team': 'Red Bull Racing', 'points': 260},
            {'driver': 'ALO', 'name': 'Fernando Alonso', 'team': 'Aston Martin', 'points': 240},
            {'driver': 'STR', 'name': 'Lance Stroll', 'team': 'Aston Martin', 'points': 185},
            {'driver': 'ALB', 'name': 'Alexander Albon', 'team': 'Williams', 'points': 165},
            {'driver': 'OCO', 'name': 'Esteban Ocon', 'team': 'Haas', 'points': 140},
            {'driver': 'HUL', 'name': 'Nico Hülkenberg', 'team': 'Haas', 'points': 125},
            {'driver': 'TSU', 'name': 'Yuki Tsunoda', 'team': 'Visa RB', 'points': 95},
            {'driver': 'LAW', 'name': 'Liam Lawson', 'team': 'Visa RB', 'points': 75},
            {'driver': 'GAS', 'name': 'Pierre Gasly', 'team': 'Alpine', 'points': 65},
            {'driver': 'DOO', 'name': 'Jack Doohan', 'team': 'Alpine', 'points': 45},
            {'driver': 'MAG', 'name': 'Kevin Magnussen', 'team': 'Sauber', 'points': 25},
            {'driver': 'BOT', 'name': 'Valtteri Bottas', 'team': 'Sauber', 'points': 15}
        ]
        
        mock_constructors = [
            {'team': 'Red Bull Racing', 'points': 835},
            {'team': 'Ferrari', 'points': 830},
            {'team': 'McLaren', 'points': 780},
            {'team': 'Mercedes', 'points': 340},
            {'team': 'Williams', 'points': 450},
            {'team': 'Aston Martin', 'points': 425},
            {'team': 'Haas', 'points': 265},
            {'team': 'Visa RB', 'points': 170},
            {'team': 'Alpine', 'points': 110},
            {'team': 'Sauber', 'points': 40}
        ]
        
        return {
            'drivers': mock_drivers,
            'constructors': mock_constructors
        }

    def _calculate_historical_standings(self, year):
        """Calculate standings from historical race data"""
        try:
            # This would require loading all races from the season
            # For now, return empty data
            return {'drivers': [], 'constructors': []}
        except Exception as e:
            self.logger.error(f"Error calculating historical standings: {str(e)}")
            return {'drivers': [], 'constructors': []} 