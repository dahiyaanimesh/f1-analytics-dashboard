import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { YEARS } from '../constants/drivers';

interface PredictionData {
  winner_prediction: {
    driver: string;
    probability: number;
  };
  podium_predictions: Array<{
    driver: string;
    probability: number;
  }>;
  points_predictions: Array<{
    driver: string;
    probability: number;
  }>;
  race_info: {
    round: number;
    race_name: string;
    circuit: string;
    date: string;
  };
}

interface RaceOption {
  round: number;
  name: string;
  circuit: string;
  date: string;
}

const RacePrediction: React.FC = () => {
  const [year, setYear] = useState(2025);
  const [selectedRace, setSelectedRace] = useState(1);
  const [predictionData, setPredictionData] = useState<PredictionData | null>(null);
  const [races, setRaces] = useState<RaceOption[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchRaces = useCallback(async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/races?year=${year}`);
      if (response.data.success && response.data.data.length > 0) {
        setRaces(response.data.data);
      } else {
        // Fallback for years without data
        console.log(`No race data available for ${year}, using fallback`);
        setRaces([]);
      }
    } catch (err) {
      console.error('Error fetching races:', err);
      setRaces([]);
    }
  }, [year]);

  useEffect(() => {
    fetchRaces();
  }, [fetchRaces]);

  // Reset selected race when year changes and races are updated
  useEffect(() => {
    if (races.length > 0 && !races.find(race => race.round === selectedRace)) {
      setSelectedRace(races[0].round);
    }
  }, [races, selectedRace]);

  const fetchPredictions = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:5000/api/predict-race', {
        year,
        round: selectedRace
      });
      
      if (response.data.success) {
        setPredictionData(response.data.data);
      } else {
        setError(response.data.error || 'Failed to fetch predictions');
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Error fetching predictions');
    } finally {
      setLoading(false);
    }
  };

  const getProbabilityColor = (probability: number) => {
    if (probability >= 0.7) return 'text-green-400';
    if (probability >= 0.4) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getProbabilityBg = (probability: number) => {
    if (probability >= 0.7) return 'bg-green-500';
    if (probability >= 0.4) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="space-y-6">
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Race Outcome Predictions</h2>
        
        {/* Controls */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Season</label>
            <select
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-red-500"
            >
              {YEARS.map(year => (
                <option key={year} value={year}>{year}</option>
              ))}
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">Race</label>
            <select
              value={selectedRace}
              onChange={(e) => setSelectedRace(Number(e.target.value))}
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-red-500"
              disabled={races.length === 0}
            >
              {races.length > 0 ? (
                races.map((race) => (
                  <option key={race.round} value={race.round}>
                    Round {race.round}: {race.name}
                  </option>
                ))
              ) : (
                <option value="">No races available for {year}</option>
              )}
            </select>
          </div>
          
          <div className="flex items-end">
            <button
              onClick={fetchPredictions}
              disabled={loading || races.length === 0}
              className="w-full bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
            >
              {loading ? 'Predicting...' : races.length === 0 ? 'No Races Available' : 'Generate Predictions'}
            </button>
          </div>
        </div>

        {error && (
          <div className="bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Predictions Display */}
        {predictionData && (
          <div className="space-y-6">
            {/* Race Info */}
            <div className="bg-gray-700 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-white mb-2">Race Information</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-gray-400">Round:</span>
                  <p className="text-white font-medium">{predictionData.race_info.round}</p>
                </div>
                <div>
                  <span className="text-gray-400">Race:</span>
                  <p className="text-white font-medium">{predictionData.race_info.race_name}</p>
                </div>
                <div>
                  <span className="text-gray-400">Circuit:</span>
                  <p className="text-white font-medium">{predictionData.race_info.circuit}</p>
                </div>
                <div>
                  <span className="text-gray-400">Date:</span>
                  <p className="text-white font-medium">{predictionData.race_info.date}</p>
                </div>
              </div>
            </div>

            {/* Winner Prediction */}
            <div className="bg-gray-700 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-white mb-4">Race Winner Prediction</h3>
              <div className="flex items-center justify-between bg-gray-800 rounded-lg p-4">
                <div>
                  <p className="text-2xl font-bold text-white">{predictionData.winner_prediction.driver}</p>
                  <p className="text-gray-400">Most likely winner</p>
                </div>
                <div className="text-right">
                  <p className={`text-2xl font-bold ${getProbabilityColor(predictionData.winner_prediction.probability)}`}>
                    {(predictionData.winner_prediction.probability * 100).toFixed(1)}%
                  </p>
                  <p className="text-gray-400">Confidence</p>
                </div>
              </div>
            </div>

            {/* Podium Predictions */}
            <div className="bg-gray-700 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-white mb-4">Podium Predictions</h3>
              <div className="space-y-3">
                {predictionData.podium_predictions.slice(0, 8).map((prediction, index) => (
                  <div key={prediction.driver} className="flex items-center justify-between bg-gray-800 rounded-lg p-3">
                    <div className="flex items-center space-x-3">
                      <span className="text-gray-400 font-mono w-6">#{index + 1}</span>
                      <span className="text-white font-medium">{prediction.driver}</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className={`font-medium ${getProbabilityColor(prediction.probability)}`}>
                        {(prediction.probability * 100).toFixed(1)}%
                      </span>
                      <div className="w-20 bg-gray-600 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${getProbabilityBg(prediction.probability)}`}
                          style={{ width: `${prediction.probability * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Points Predictions */}
            <div className="bg-gray-700 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-white mb-4">Points Scoring Predictions</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {predictionData.points_predictions.slice(0, 10).map((prediction, index) => (
                  <div key={prediction.driver} className="flex items-center justify-between bg-gray-800 rounded-lg p-3">
                    <div className="flex items-center space-x-3">
                      <span className="text-gray-400 font-mono w-6">#{index + 1}</span>
                      <span className="text-white font-medium">{prediction.driver}</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <span className={`font-medium ${getProbabilityColor(prediction.probability)}`}>
                        {(prediction.probability * 100).toFixed(1)}%
                      </span>
                      <div className="w-16 bg-gray-600 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${getProbabilityBg(prediction.probability)}`}
                          style={{ width: `${prediction.probability * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {!predictionData && !loading && (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-4a2 2 0 01-2-2z" />
              </svg>
            </div>
            <p className="text-gray-400">Select a race and generate predictions to see ML-powered race outcome forecasts</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default RacePrediction; 