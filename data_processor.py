import fastf1
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging
import os

# Ensure cache directory exists and enable FastF1 cache
cache_dir = 'cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)
    print(f"📁 Created cache directory: {cache_dir}")

fastf1.Cache.enable_cache(cache_dir)

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
        
        # Historical race calendars for common years
        self.historical_races = {
            2024: [
                {'round': 1, 'name': 'Bahrain Grand Prix', 'location': 'Sakhir', 'country': 'Bahrain', 'circuit': 'Bahrain International Circuit', 'date': '2024-03-02'},
                {'round': 2, 'name': 'Saudi Arabian Grand Prix', 'location': 'Jeddah', 'country': 'Saudi Arabia', 'circuit': 'Jeddah Corniche Circuit', 'date': '2024-03-09'},
                {'round': 3, 'name': 'Australian Grand Prix', 'location': 'Melbourne', 'country': 'Australia', 'circuit': 'Albert Park Circuit', 'date': '2024-03-24'},
                {'round': 4, 'name': 'Japanese Grand Prix', 'location': 'Suzuka', 'country': 'Japan', 'circuit': 'Suzuka Circuit', 'date': '2024-04-07'},
                {'round': 5, 'name': 'Chinese Grand Prix', 'location': 'Shanghai', 'country': 'China', 'circuit': 'Shanghai International Circuit', 'date': '2024-04-21'},
                {'round': 6, 'name': 'Miami Grand Prix', 'location': 'Miami', 'country': 'USA', 'circuit': 'Miami International Autodrome', 'date': '2024-05-05'},
                {'round': 7, 'name': 'Emilia Romagna Grand Prix', 'location': 'Imola', 'country': 'Italy', 'circuit': 'Autodromo Enzo e Dino Ferrari', 'date': '2024-05-19'},
                {'round': 8, 'name': 'Monaco Grand Prix', 'location': 'Monte Carlo', 'country': 'Monaco', 'circuit': 'Circuit de Monaco', 'date': '2024-05-26'},
                {'round': 9, 'name': 'Canadian Grand Prix', 'location': 'Montreal', 'country': 'Canada', 'circuit': 'Circuit Gilles Villeneuve', 'date': '2024-06-09'},
                {'round': 10, 'name': 'Spanish Grand Prix', 'location': 'Barcelona', 'country': 'Spain', 'circuit': 'Circuit de Barcelona-Catalunya', 'date': '2024-06-23'},
                {'round': 11, 'name': 'Austrian Grand Prix', 'location': 'Spielberg', 'country': 'Austria', 'circuit': 'Red Bull Ring', 'date': '2024-06-30'},
                {'round': 12, 'name': 'British Grand Prix', 'location': 'Silverstone', 'country': 'United Kingdom', 'circuit': 'Silverstone Circuit', 'date': '2024-07-07'},
                {'round': 13, 'name': 'Hungarian Grand Prix', 'location': 'Budapest', 'country': 'Hungary', 'circuit': 'Hungaroring', 'date': '2024-07-21'},
                {'round': 14, 'name': 'Belgian Grand Prix', 'location': 'Spa-Francorchamps', 'country': 'Belgium', 'circuit': 'Circuit de Spa-Francorchamps', 'date': '2024-07-28'},
                {'round': 15, 'name': 'Dutch Grand Prix', 'location': 'Zandvoort', 'country': 'Netherlands', 'circuit': 'Circuit Zandvoort', 'date': '2024-08-25'},
                {'round': 16, 'name': 'Italian Grand Prix', 'location': 'Monza', 'country': 'Italy', 'circuit': 'Autodromo Nazionale di Monza', 'date': '2024-09-01'},
                {'round': 17, 'name': 'Azerbaijan Grand Prix', 'location': 'Baku', 'country': 'Azerbaijan', 'circuit': 'Baku City Circuit', 'date': '2024-09-15'},
                {'round': 18, 'name': 'Singapore Grand Prix', 'location': 'Singapore', 'country': 'Singapore', 'circuit': 'Marina Bay Street Circuit', 'date': '2024-09-22'},
                {'round': 19, 'name': 'United States Grand Prix', 'location': 'Austin', 'country': 'USA', 'circuit': 'Circuit of the Americas', 'date': '2024-10-20'},
                {'round': 20, 'name': 'Mexico City Grand Prix', 'location': 'Mexico City', 'country': 'Mexico', 'circuit': 'Autódromo Hermanos Rodríguez', 'date': '2024-10-27'},
                {'round': 21, 'name': 'São Paulo Grand Prix', 'location': 'São Paulo', 'country': 'Brazil', 'circuit': 'Interlagos', 'date': '2024-11-03'},
                {'round': 22, 'name': 'Las Vegas Grand Prix', 'location': 'Las Vegas', 'country': 'USA', 'circuit': 'Las Vegas Strip Street Circuit', 'date': '2024-11-23'},
                {'round': 23, 'name': 'Qatar Grand Prix', 'location': 'Lusail', 'country': 'Qatar', 'circuit': 'Lusail International Circuit', 'date': '2024-12-01'},
                {'round': 24, 'name': 'Abu Dhabi Grand Prix', 'location': 'Abu Dhabi', 'country': 'UAE', 'circuit': 'Yas Marina Circuit', 'date': '2024-12-08'}
            ],
            2023: [
                {'round': 1, 'name': 'Bahrain Grand Prix', 'location': 'Sakhir', 'country': 'Bahrain', 'circuit': 'Bahrain International Circuit', 'date': '2023-03-05'},
                {'round': 2, 'name': 'Saudi Arabian Grand Prix', 'location': 'Jeddah', 'country': 'Saudi Arabia', 'circuit': 'Jeddah Corniche Circuit', 'date': '2023-03-19'},
                {'round': 3, 'name': 'Australian Grand Prix', 'location': 'Melbourne', 'country': 'Australia', 'circuit': 'Albert Park Circuit', 'date': '2023-04-02'},
                {'round': 4, 'name': 'Azerbaijan Grand Prix', 'location': 'Baku', 'country': 'Azerbaijan', 'circuit': 'Baku City Circuit', 'date': '2023-04-30'},
                {'round': 5, 'name': 'Miami Grand Prix', 'location': 'Miami', 'country': 'USA', 'circuit': 'Miami International Autodrome', 'date': '2023-05-07'},
                {'round': 6, 'name': 'Monaco Grand Prix', 'location': 'Monte Carlo', 'country': 'Monaco', 'circuit': 'Circuit de Monaco', 'date': '2023-05-28'},
                {'round': 7, 'name': 'Spanish Grand Prix', 'location': 'Barcelona', 'country': 'Spain', 'circuit': 'Circuit de Barcelona-Catalunya', 'date': '2023-06-04'},
                {'round': 8, 'name': 'Canadian Grand Prix', 'location': 'Montreal', 'country': 'Canada', 'circuit': 'Circuit Gilles Villeneuve', 'date': '2023-06-18'},
                {'round': 9, 'name': 'Austrian Grand Prix', 'location': 'Spielberg', 'country': 'Austria', 'circuit': 'Red Bull Ring', 'date': '2023-07-02'},
                {'round': 10, 'name': 'British Grand Prix', 'location': 'Silverstone', 'country': 'United Kingdom', 'circuit': 'Silverstone Circuit', 'date': '2023-07-09'},
                {'round': 11, 'name': 'Hungarian Grand Prix', 'location': 'Budapest', 'country': 'Hungary', 'circuit': 'Hungaroring', 'date': '2023-07-23'},
                {'round': 12, 'name': 'Belgian Grand Prix', 'location': 'Spa-Francorchamps', 'country': 'Belgium', 'circuit': 'Circuit de Spa-Francorchamps', 'date': '2023-07-30'},
                {'round': 13, 'name': 'Dutch Grand Prix', 'location': 'Zandvoort', 'country': 'Netherlands', 'circuit': 'Circuit Zandvoort', 'date': '2023-08-27'},
                {'round': 14, 'name': 'Italian Grand Prix', 'location': 'Monza', 'country': 'Italy', 'circuit': 'Autodromo Nazionale di Monza', 'date': '2023-09-03'},
                {'round': 15, 'name': 'Singapore Grand Prix', 'location': 'Singapore', 'country': 'Singapore', 'circuit': 'Marina Bay Street Circuit', 'date': '2023-09-17'},
                {'round': 16, 'name': 'Japanese Grand Prix', 'location': 'Suzuka', 'country': 'Japan', 'circuit': 'Suzuka Circuit', 'date': '2023-09-24'},
                {'round': 17, 'name': 'Qatar Grand Prix', 'location': 'Lusail', 'country': 'Qatar', 'circuit': 'Lusail International Circuit', 'date': '2023-10-08'},
                {'round': 18, 'name': 'United States Grand Prix', 'location': 'Austin', 'country': 'USA', 'circuit': 'Circuit of the Americas', 'date': '2023-10-22'},
                {'round': 19, 'name': 'Mexico City Grand Prix', 'location': 'Mexico City', 'country': 'Mexico', 'circuit': 'Autódromo Hermanos Rodríguez', 'date': '2023-10-29'},
                {'round': 20, 'name': 'São Paulo Grand Prix', 'location': 'São Paulo', 'country': 'Brazil', 'circuit': 'Interlagos', 'date': '2023-11-05'},
                {'round': 21, 'name': 'Las Vegas Grand Prix', 'location': 'Las Vegas', 'country': 'USA', 'circuit': 'Las Vegas Strip Street Circuit', 'date': '2023-11-18'},
                {'round': 22, 'name': 'Abu Dhabi Grand Prix', 'location': 'Abu Dhabi', 'country': 'UAE', 'circuit': 'Yas Marina Circuit', 'date': '2023-11-26'}
            ]
        }

    def get_season_races(self, year):
        """Get race calendar for a given year with robust fallback"""
        try:
            # First priority: predefined race calendars
            if year == 2025:
                return self.races_2025
            elif year in self.historical_races:
                return self.historical_races[year]
            
            # Second priority: try FastF1 for historical data
            try:
                schedule = fastf1.get_event_schedule(year)
                if not schedule.empty:
                    races = []
                    for idx, event in schedule.iterrows():
                        if event.get('EventFormat') == 'conventional' or pd.isna(event.get('EventFormat')):
                            race_data = {
                                'round': int(event.get('RoundNumber', idx + 1)),
                                'name': str(event.get('EventName', f'Race {idx + 1}')),
                                'location': str(event.get('Location', 'Unknown')),
                                'country': str(event.get('Country', 'Unknown')),
                                'circuit': str(event.get('EventName', f'Circuit {idx + 1}')),
                                'date': event['EventDate'].strftime('%Y-%m-%d') if pd.notna(event.get('EventDate')) else f'{year}-01-01'
                            }
                            races.append(race_data)
                    
                    if races:
                        return races
            except Exception as e:
                self.logger.warning(f"FastF1 schedule unavailable for {year}: {str(e)}")
            
            # Third priority: generate a generic season calendar
            return self._generate_generic_season(year)
            
        except Exception as e:
            self.logger.error(f"Error getting season races for {year}: {str(e)}")
            return self._generate_generic_season(year)

    def _generate_generic_season(self, year):
        """Generate a generic F1 season with standard races"""
        generic_races = [
            {'name': 'Bahrain Grand Prix', 'location': 'Sakhir', 'country': 'Bahrain', 'circuit': 'Bahrain International Circuit'},
            {'name': 'Saudi Arabian Grand Prix', 'location': 'Jeddah', 'country': 'Saudi Arabia', 'circuit': 'Jeddah Corniche Circuit'},
            {'name': 'Australian Grand Prix', 'location': 'Melbourne', 'country': 'Australia', 'circuit': 'Albert Park Circuit'},
            {'name': 'Japanese Grand Prix', 'location': 'Suzuka', 'country': 'Japan', 'circuit': 'Suzuka Circuit'},
            {'name': 'Chinese Grand Prix', 'location': 'Shanghai', 'country': 'China', 'circuit': 'Shanghai International Circuit'},
            {'name': 'Miami Grand Prix', 'location': 'Miami', 'country': 'USA', 'circuit': 'Miami International Autodrome'},
            {'name': 'Emilia Romagna Grand Prix', 'location': 'Imola', 'country': 'Italy', 'circuit': 'Autodromo Enzo e Dino Ferrari'},
            {'name': 'Monaco Grand Prix', 'location': 'Monte Carlo', 'country': 'Monaco', 'circuit': 'Circuit de Monaco'},
            {'name': 'Canadian Grand Prix', 'location': 'Montreal', 'country': 'Canada', 'circuit': 'Circuit Gilles Villeneuve'},
            {'name': 'Spanish Grand Prix', 'location': 'Barcelona', 'country': 'Spain', 'circuit': 'Circuit de Barcelona-Catalunya'},
            {'name': 'Austrian Grand Prix', 'location': 'Spielberg', 'country': 'Austria', 'circuit': 'Red Bull Ring'},
            {'name': 'British Grand Prix', 'location': 'Silverstone', 'country': 'United Kingdom', 'circuit': 'Silverstone Circuit'},
            {'name': 'Hungarian Grand Prix', 'location': 'Budapest', 'country': 'Hungary', 'circuit': 'Hungaroring'},
            {'name': 'Belgian Grand Prix', 'location': 'Spa-Francorchamps', 'country': 'Belgium', 'circuit': 'Circuit de Spa-Francorchamps'},
            {'name': 'Dutch Grand Prix', 'location': 'Zandvoort', 'country': 'Netherlands', 'circuit': 'Circuit Zandvoort'},
            {'name': 'Italian Grand Prix', 'location': 'Monza', 'country': 'Italy', 'circuit': 'Autodromo Nazionale di Monza'},
            {'name': 'Singapore Grand Prix', 'location': 'Singapore', 'country': 'Singapore', 'circuit': 'Marina Bay Street Circuit'},
            {'name': 'United States Grand Prix', 'location': 'Austin', 'country': 'USA', 'circuit': 'Circuit of the Americas'},
            {'name': 'Mexico City Grand Prix', 'location': 'Mexico City', 'country': 'Mexico', 'circuit': 'Autódromo Hermanos Rodríguez'},
            {'name': 'São Paulo Grand Prix', 'location': 'São Paulo', 'country': 'Brazil', 'circuit': 'Interlagos'},
            {'name': 'Abu Dhabi Grand Prix', 'location': 'Abu Dhabi', 'country': 'UAE', 'circuit': 'Yas Marina Circuit'}
        ]
        
        races = []
        for i, race_info in enumerate(generic_races):
            races.append({
                'round': i + 1,
                'name': race_info['name'],
                'location': race_info['location'],
                'country': race_info['country'],
                'circuit': race_info['circuit'],
                'date': f'{year}-{3 + i//4:02d}-{1 + (i*7)%28:02d}'  # Generate reasonable dates
            })
        
        return races

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
        """Mock standings for 2025 season - Updated without Bottas and Perez"""
        mock_drivers = [
            {'driver': 'PIA', 'name': 'Oscar Piastri', 'team': 'McLaren Mercedes', 'points': 161},
            {'driver': 'NOR', 'name': 'Lando Norris', 'team': 'McLaren Mercedes', 'points': 158},
            {'driver': 'VER', 'name': 'Max Verstappen', 'team': 'Red Bull Racing Honda RBPT', 'points': 136},
            {'driver': 'RUS', 'name': 'George Russell', 'team': 'Mercedes', 'points': 99},
            {'driver': 'LEC', 'name': 'Charles Leclerc', 'team': 'Ferrari', 'points': 79},
            {'driver': 'HAM', 'name': 'Lewis Hamilton', 'team': 'Ferrari', 'points': 63},
            {'driver': 'ANT', 'name': 'Kimi Antonelli', 'team': 'Mercedes', 'points': 48},
            {'driver': 'ALB', 'name': 'Alexander Albon', 'team': 'Williams Mercedes', 'points': 42},
            {'driver': 'OCO', 'name': 'Esteban Ocon', 'team': 'Haas Ferrari', 'points': 20},
            {'driver': 'HAD', 'name': 'Isack Hadjar', 'team': 'Racing Bulls Honda RBPT', 'points': 15},
            {'driver': 'STR', 'name': 'Lance Stroll', 'team': 'Aston Martin Aramco Mercedes', 'points': 14},
            {'driver': 'SAI', 'name': 'Carlos Sainz', 'team': 'Williams Mercedes', 'points': 12},
            {'driver': 'ALO', 'name': 'Fernando Alonso', 'team': 'Aston Martin Aramco Mercedes', 'points': 6},
            {'driver': 'TSU', 'name': 'Yuki Tsunoda', 'team': 'Racing Bulls Honda RBPT', 'points': 4},
            {'driver': 'HUL', 'name': 'Nico Hülkenberg', 'team': 'Haas Ferrari', 'points': 2},
            {'driver': 'GAS', 'name': 'Pierre Gasly', 'team': 'Alpine Renault', 'points': 1},
            {'driver': 'DOO', 'name': 'Jack Doohan', 'team': 'Alpine Renault', 'points': 0},
            {'driver': 'LAW', 'name': 'Liam Lawson', 'team': 'Red Bull Racing Honda RBPT', 'points': 0},
            {'driver': 'COL', 'name': 'Franco Colapinto', 'team': 'Kick Sauber Ferrari', 'points': 0},
            {'driver': 'BEA', 'name': 'Oliver Bearman', 'team': 'Kick Sauber Ferrari', 'points': 0}
        ]
        
        mock_constructors = [
            {'team': 'McLaren Mercedes', 'points': 319},
            {'team': 'Mercedes', 'points': 147},
            {'team': 'Red Bull Racing Honda RBPT', 'points': 136},
            {'team': 'Ferrari', 'points': 142},
            {'team': 'Williams Mercedes', 'points': 54},
            {'team': 'Haas Ferrari', 'points': 22},
            {'team': 'Racing Bulls Honda RBPT', 'points': 19},
            {'team': 'Aston Martin Aramco Mercedes', 'points': 20},
            {'team': 'Alpine Renault', 'points': 1},
            {'team': 'Kick Sauber Ferrari', 'points': 0}
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