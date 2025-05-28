from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback

# Import our modules
from data_processor import DataProcessor
from driver_analyzer import DriverAnalyzer
from strategy_optimizer import StrategyOptimizer
from race_predictor import RacePredictor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components
data_processor = DataProcessor()
driver_analyzer = DriverAnalyzer()
strategy_optimizer = StrategyOptimizer()
race_predictor = RacePredictor()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'F1 Analytics API is running'
    })

@app.route('/api/races', methods=['GET'])
def get_races():
    """Get race calendar for a given year"""
    try:
        year = request.args.get('year', 2025, type=int)
        races = data_processor.get_season_races(year)
        
        return jsonify({
            'success': True,
            'data': races
        })
    except Exception as e:
        logger.error(f"Error fetching races: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/race-data/<int:year>/<int:round_num>', methods=['GET'])
def get_race_data(year, round_num):
    """Get detailed race data"""
    try:
        race_data = data_processor.get_race_data(year, round_num)
        
        return jsonify({
            'success': True,
            'data': race_data
        })
    except Exception as e:
        logger.error(f"Error fetching race data: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/strategy-optimization', methods=['POST'])
def optimize_strategy():
    """Optimize pit stop strategy"""
    try:
        data = request.get_json()
        year = data.get('year', 2025)
        round_num = data.get('round', 1)
        driver = data.get('driver', 'VER')
        
        result = strategy_optimizer.optimize_pit_strategy(year, round_num, driver)
        
        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        logger.error(f"Error optimizing strategy: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/driver-performance/<driver>', methods=['GET'])
def get_driver_performance(driver):
    """Get driver performance analysis"""
    try:
        year = request.args.get('year', 2025, type=int)
        performance_data = driver_analyzer.analyze_driver_performance(driver, year)
        
        return jsonify({
            'success': True,
            'data': performance_data
        })
    except Exception as e:
        logger.error(f"Error analyzing driver performance: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/driver-comparison', methods=['POST'])
def compare_drivers():
    """Compare multiple drivers"""
    try:
        data = request.get_json()
        drivers = data.get('drivers', ['VER', 'LEC'])
        year = data.get('year', 2025)
        
        comparison_data = driver_analyzer.compare_drivers(drivers, year)
        
        return jsonify({
            'success': True,
            'data': comparison_data
        })
    except Exception as e:
        logger.error(f"Error comparing drivers: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predict-race', methods=['POST'])
def predict_race():
    """Predict race outcomes"""
    try:
        data = request.get_json()
        year = data.get('year', 2025)
        round_num = data.get('round', 1)
        
        predictions = race_predictor.predict_race_outcome(year, round_num)
        
        return jsonify({
            'success': True,
            'data': predictions
        })
    except Exception as e:
        logger.error(f"Error predicting race: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/season-standings/<int:year>', methods=['GET'])
def get_season_standings(year):
    """Get championship standings for a season"""
    try:
        standings = data_processor.get_season_standings(year)
        
        return jsonify({
            'success': True,
            'data': standings
        })
    except Exception as e:
        logger.error(f"Error fetching standings: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("Starting F1 Analytics API...")
    print("Available endpoints:")
    print("  GET  /api/health")
    print("  GET  /api/races?year=2025")
    print("  GET  /api/race-data/{year}/{round}")
    print("  POST /api/strategy-optimization")
    print("  GET  /api/driver-performance/{driver}")
    print("  POST /api/driver-comparison")
    print("  POST /api/predict-race")
    print("  GET  /api/season-standings/{year}")
    print("\nServer running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000) 