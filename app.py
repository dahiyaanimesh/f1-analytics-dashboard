from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import traceback
import sys
import gc

# Import our modules
from data_processor import DataProcessor
from driver_analyzer import DriverAnalyzer
from strategy_optimizer import StrategyOptimizer
from race_predictor import EnhancedRacePredictor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('f1_api.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize components with error handling
def initialize_components():
    """Initialize all components with error handling"""
    try:
        data_processor = DataProcessor()
        logger.info("✅ DataProcessor initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize DataProcessor: {e}")
        data_processor = None

    try:
        driver_analyzer = DriverAnalyzer()
        logger.info("✅ DriverAnalyzer initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize DriverAnalyzer: {e}")
        driver_analyzer = None

    try:
        strategy_optimizer = StrategyOptimizer()
        logger.info("✅ StrategyOptimizer initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize StrategyOptimizer: {e}")
        strategy_optimizer = None

    try:
        race_predictor = EnhancedRacePredictor()
        logger.info("✅ EnhancedRacePredictor initialized")
    except Exception as e:
        logger.error(f"❌ Failed to initialize EnhancedRacePredictor: {e}")
        race_predictor = None

    return data_processor, driver_analyzer, strategy_optimizer, race_predictor

# Initialize components
data_processor, driver_analyzer, strategy_optimizer, race_predictor = initialize_components()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    try:
        component_status = {
            'data_processor': data_processor is not None,
            'driver_analyzer': driver_analyzer is not None,
            'strategy_optimizer': strategy_optimizer is not None,
            'race_predictor': race_predictor is not None
        }
        
        return jsonify({
            'status': 'healthy',
            'message': 'F1 Analytics API is running',
            'components': component_status,
            'timestamp': str(pd.Timestamp.now())
        })
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/races', methods=['GET'])
def get_races():
    """Get race calendar for a given year"""
    try:
        if not data_processor:
            return jsonify({
                'success': False,
                'error': 'DataProcessor not available'
            }), 503

        year = request.args.get('year', 2025, type=int)
        logger.info(f"[RACES] Fetching races for year {year}")
        
        races = data_processor.get_season_races(year)
        
        if not races:
            logger.warning(f"No races found for year {year}")
            return jsonify({
                'success': False,
                'error': f'No races available for year {year}'
            }), 404
        
        logger.info(f"[SUCCESS] Found {len(races)} races for {year}")
        return jsonify({
            'success': True,
            'data': races,
            'count': len(races)
        })
        
    except Exception as e:
        logger.error(f"❌ Error fetching races: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Clean up any potential memory issues
        gc.collect()
        
        return jsonify({
            'success': False,
            'error': f'Error fetching races: {str(e)}'
        }), 500

@app.route('/api/race-data/<int:year>/<int:round_num>', methods=['GET'])
def get_race_data(year, round_num):
    """Get detailed race data"""
    try:
        if not data_processor:
            return jsonify({
                'success': False,
                'error': 'DataProcessor not available'
            }), 503

        logger.info(f"[RACE] Fetching race data for {year} Round {round_num}")
        race_data = data_processor.get_race_data(year, round_num)
        
        return jsonify({
            'success': True,
            'data': race_data
        })
        
    except Exception as e:
        logger.error(f"[ERROR] Error fetching race data: {str(e)}")
        logger.error(traceback.format_exc())
        gc.collect()
        
        return jsonify({
            'success': False,
            'error': f'Error fetching race data: {str(e)}'
        }), 500

@app.route('/api/strategy-optimization', methods=['POST'])
def optimize_strategy():
    """Optimize pit stop strategy"""
    try:
        if not strategy_optimizer:
            return jsonify({
                'success': False,
                'error': 'StrategyOptimizer not available'
            }), 503

        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400

        year = data.get('year', 2025)
        round_num = data.get('round', 1)
        driver = data.get('driver', 'VER')
        
        logger.info(f"[STRATEGY] Optimizing strategy for {driver} - {year} Round {round_num}")
        
        result = strategy_optimizer.optimize_pit_strategy(year, round_num, driver)
        
        logger.info(f"[SUCCESS] Strategy optimization completed for {driver}")
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"❌ Error optimizing strategy: {str(e)}")
        logger.error(traceback.format_exc())
        gc.collect()
        
        return jsonify({
            'success': False,
            'error': f'Error optimizing strategy: {str(e)}'
        }), 500

@app.route('/api/driver-performance/<driver>', methods=['GET'])
def get_driver_performance(driver):
    """Get driver performance analysis"""
    try:
        if not driver_analyzer:
            return jsonify({
                'success': False,
                'error': 'DriverAnalyzer not available'
            }), 503

        year = request.args.get('year', 2025, type=int)
        logger.info(f"[DRIVER] Analyzing performance for driver {driver} in {year}")
        
        performance_data = driver_analyzer.analyze_driver_performance(driver, year)
        
        return jsonify({
            'success': True,
            'data': performance_data
        })
        
    except Exception as e:
        logger.error(f"[ERROR] Error analyzing driver performance: {str(e)}")
        logger.error(traceback.format_exc())
        gc.collect()
        
        return jsonify({
            'success': False,
            'error': f'Error analyzing driver performance: {str(e)}'
        }), 500

@app.route('/api/driver-comparison', methods=['POST'])
def compare_drivers():
    """Compare multiple drivers"""
    try:
        if not driver_analyzer:
            return jsonify({
                'success': False,
                'error': 'DriverAnalyzer not available'
            }), 503

        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400

        drivers = data.get('drivers', ['VER', 'LEC'])
        year = data.get('year', 2025)
        
        logger.info(f"[COMPARISON] Comparing drivers {drivers} for {year}")
        
        comparison_data = driver_analyzer.compare_drivers(drivers, year)
        
        return jsonify({
            'success': True,
            'data': comparison_data
        })
        
    except Exception as e:
        logger.error(f"[ERROR] Error comparing drivers: {str(e)}")
        logger.error(traceback.format_exc())
        gc.collect()
        
        return jsonify({
            'success': False,
            'error': f'Error comparing drivers: {str(e)}'
        }), 500

@app.route('/api/predict-race', methods=['POST'])
def predict_race():
    """Predict race outcomes"""
    try:
        if not race_predictor:
            return jsonify({
                'success': False,
                'error': 'RacePredictor not available'
            }), 503

        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400

        year = data.get('year', 2025)
        round_num = data.get('round', 1)
        
        logger.info(f"[PREDICTION] Predicting race for {year} Round {round_num}")
        
        predictions = race_predictor.predict_race_outcome(year, round_num)
        
        return jsonify({
            'success': True,
            'data': predictions
        })
        
    except Exception as e:
        logger.error(f"[ERROR] Error predicting race: {str(e)}")
        logger.error(traceback.format_exc())
        gc.collect()
        
        return jsonify({
            'success': False,
            'error': f'Error predicting race: {str(e)}'
        }), 500

@app.route('/api/detailed-race-analysis', methods=['POST'])
def detailed_race_analysis():
    """Get detailed race analysis with full predictions and confidence metrics"""
    try:
        if not race_predictor:
            return jsonify({
                'success': False,
                'error': 'EnhancedRacePredictor not available'
            }), 503

        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400

        year = data.get('year', 2025)
        round_num = data.get('round', 1)
        
        logger.info(f"[DETAILED ANALYSIS] Performing detailed race analysis for {year} Round {round_num}")
        
        # Get comprehensive predictions
        predictions = race_predictor.predict_race_outcome(year, round_num)
        
        # Add additional analysis if available
        analysis_data = {
            'predictions': predictions,
            'analysis_metadata': {
                'model_type': 'Enhanced ML-based Predictor',
                'features_used': [
                    'Driver skill ratings', 'Team performance', 'Track characteristics',
                    'Historical performance', 'Dynamic factors', 'Weather conditions',
                    'Championship pressure', 'Driver-team synergy'
                ],
                'prediction_accuracy': 'Based on comprehensive 29-feature ML model',
                'last_updated': str(pd.Timestamp.now())
            }
        }
        
        # If full predictions are available, add position-by-position breakdown
        if 'full_predictions' in predictions:
            analysis_data['position_breakdown'] = sorted(
                predictions['full_predictions'], 
                key=lambda x: x['predicted_position']
            )
        
        logger.info(f"[SUCCESS] Detailed analysis completed for {year} Round {round_num}")
        return jsonify({
            'success': True,
            'data': analysis_data
        })
        
    except Exception as e:
        logger.error(f"[ERROR] Error in detailed race analysis: {str(e)}")
        logger.error(traceback.format_exc())
        gc.collect()
        
        return jsonify({
            'success': False,
            'error': f'Error in detailed race analysis: {str(e)}'
        }), 500

@app.route('/api/season-standings/<int:year>', methods=['GET'])
def get_season_standings(year):
    """Get championship standings for a season"""
    try:
        if not data_processor:
            return jsonify({
                'success': False,
                'error': 'DataProcessor not available'
            }), 503

        logger.info(f"[STANDINGS] Fetching standings for {year}")
        
        standings = data_processor.get_season_standings(year)
        
        if not standings or (not standings.get('drivers') and not standings.get('constructors')):
            logger.warning(f"No standings found for year {year}")
            return jsonify({
                'success': False,
                'error': f'No standings available for year {year}'
            }), 404
        
        return jsonify({
            'success': True,
            'data': standings
        })
        
    except Exception as e:
        logger.error(f"[ERROR] Error fetching standings: {str(e)}")
        logger.error(traceback.format_exc())
        gc.collect()
        
        return jsonify({
            'success': False,
            'error': f'Error fetching standings: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 error: {error}")
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 error: {error}")
    gc.collect()  # Clean up memory on server errors
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("🏎️  Starting F1 Analytics API...")
    print("Available endpoints:")
    print("  GET  /api/health")
    print("  GET  /api/races?year=2025")
    print("  GET  /api/race-data/{year}/{round}")
    print("  POST /api/strategy-optimization")
    print("  GET  /api/driver-performance/{driver}")
    print("  POST /api/driver-comparison")
    print("  POST /api/predict-race")
    print("  POST /api/detailed-race-analysis")
    print("  GET  /api/season-standings/{year}")
    print("\n🚀 Server running on http://localhost:5000")
    
    # Import pandas for timestamps
    import pandas as pd
    
    try:
        app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1) 