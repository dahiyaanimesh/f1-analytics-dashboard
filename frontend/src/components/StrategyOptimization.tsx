import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { getDriversForYear, YEARS } from '../constants/drivers';

interface StrategyResult {
  optimal_strategy: {
    stops: number;
    stints: Array<{
      compound: string;
      laps: number;
    }>;
    pit_laps: number[];
    total_time: number;
    time_penalty: number;
  };
  actual_strategy: {
    stops?: number;
    stints?: Array<{
      compound: string;
      laps: number;
      start_lap: number;
      end_lap: number;
    }>;
    pit_laps?: number[];
    total_time?: number;
    error?: string;
  };
  time_savings: number;
  available_compounds: string[];
  track_conditions?: {
    weather: string;
    tire_degradation: number;
    overtaking_difficulty: number;
  };
}

interface RaceOption {
  round: number;
  name: string;
  circuit: string;
  date: string;
}

const StrategyOptimization: React.FC = () => {
  const [year, setYear] = useState(2025);
  const [round, setRound] = useState(1);
  const [driver, setDriver] = useState('VER');
  const [races, setRaces] = useState<RaceOption[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<StrategyResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Filter drivers for the selected year
  const availableDrivers = getDriversForYear(year);
  
  // Ensure selected driver is valid for the current year
  useEffect(() => {
    if (!availableDrivers.find(d => d.code === driver)) {
      if (availableDrivers.length > 0) {
        setDriver(availableDrivers[0].code);
      }
    }
  }, [year, availableDrivers, driver]);

  // Fetch races when year changes
  const fetchRaces = useCallback(async () => {
    try {
      const response = await axios.get(`http://localhost:5000/api/races?year=${year}`);
      if (response.data.success && response.data.data.length > 0) {
        const raceData = response.data.data.map((race: any) => ({
          round: race.round,
          name: race.name,
          circuit: race.circuit,
          date: race.date
        }));
        setRaces(raceData);
        
        // Reset round if current round doesn't exist in new year
        if (!raceData.find((race: any) => race.round === round)) {
          setRound(raceData[0]?.round || 1);
        }
      }
    } catch (err) {
      console.error('Error fetching races:', err);
    }
  }, [year, round]);

  useEffect(() => {
    fetchRaces();
  }, [fetchRaces]);

  const optimizeStrategy = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.post('http://localhost:5000/api/strategy-optimization', {
        year,
        round,
        driver
      });
      
      if (response.data.success) {
        setResult(response.data.data);
      } else {
        setError(response.data.error || 'Failed to optimize strategy');
      }
    } catch (err: any) {
      setError(err.response?.data?.error || 'Error optimizing strategy');
    } finally {
      setLoading(false);
    }
  };

  const getTireColor = (compound: string) => {
    const colors: { [key: string]: string } = {
      'SOFT': 'bg-red-500',
      'MEDIUM': 'bg-yellow-500',
      'HARD': 'bg-gray-300 text-black',
      'INTERMEDIATE': 'bg-green-500',
      'WET': 'bg-blue-500'
    };
    return colors[compound] || 'bg-gray-500';
  };

  const getWeatherIcon = (weather: string) => {
    const icons: { [key: string]: string } = {
      'dry': '☀️',
      'wet': '🌧️',
      'mixed': '⛅',
      'hot': '🔥',
      'cold': '🧊'
    };
    return icons[weather] || '🌤️';
  };

  const getDifficultyColor = (value: number) => {
    if (value >= 0.8) return 'text-red-400';
    if (value >= 0.6) return 'text-yellow-400';
    if (value >= 0.4) return 'text-green-400';
    return 'text-blue-400';
  };

  const selectedRace = races.find(race => race.round === round);

  return (
    <div className="space-y-6">
      <div className="bg-gray-800 rounded-lg p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Strategy Optimization</h2>
        <p className="text-gray-300 mb-6">Optimize pit stop strategies using race simulation</p>
        
        <div className="bg-gray-700 rounded-lg p-6 mb-6">
          <h3 className="text-lg font-semibold text-white mb-4">Race Parameters</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Year</label>
              <select
                value={year}
                onChange={(e) => setYear(Number(e.target.value))}
                className="w-full bg-gray-600 border border-gray-500 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                {YEARS.map(y => (
                  <option key={y} value={y}>{y}</option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Round</label>
              <select
                value={round}
                onChange={(e) => setRound(Number(e.target.value))}
                className="w-full bg-gray-600 border border-gray-500 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                {races.map((race) => (
                  <option key={race.round} value={race.round}>
                    Round {race.round}: {race.name}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">Driver ({availableDrivers.length} available in {year})</label>
              <select
                value={driver}
                onChange={(e) => setDriver(e.target.value)}
                className="w-full bg-gray-600 border border-gray-500 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-red-500"
              >
                {availableDrivers.map((d) => (
                  <option key={d.code} value={d.code}>
                    {d.name} ({d.code})
                  </option>
                ))}
              </select>
            </div>
          </div>
          
          <button
            onClick={optimizeStrategy}
            disabled={loading}
            className="mt-6 w-full bg-red-600 hover:bg-red-700 disabled:bg-gray-600 text-white px-6 py-3 rounded-lg font-medium transition-colors duration-200"
          >
            {loading ? 'Optimizing...' : 'Optimize Strategy'}
          </button>
        </div>

        {error && (
          <div className="bg-red-900 border border-red-700 text-red-200 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {result && (
          <div className="space-y-6">
            {/* Race Information with Track Conditions */}
            <div className="bg-gray-700 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Race Information</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-gray-400">Round:</span>
                  <p className="text-white font-medium">{round}</p>
                </div>
                <div>
                  <span className="text-gray-400">Race:</span>
                  <p className="text-white font-medium">{selectedRace?.name || 'Unknown Race'}</p>
                </div>
                <div>
                  <span className="text-gray-400">Driver:</span>
                  <p className="text-white font-medium">{availableDrivers.find(d => d.code === driver)?.name || driver}</p>
                </div>
                <div>
                  <span className="text-gray-400">Season:</span>
                  <p className="text-white font-medium">{year}</p>
                </div>
              </div>
              
              {/* Track Conditions */}
              {result.track_conditions && (
                <div className="mt-4 pt-4 border-t border-gray-600">
                  <h4 className="text-md font-medium text-white mb-3">Track Conditions</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div className="flex items-center space-x-2">
                      <span className="text-gray-400">Weather:</span>
                      <span className="text-2xl">{getWeatherIcon(result.track_conditions.weather)}</span>
                      <span className="text-white font-medium capitalize">{result.track_conditions.weather}</span>
                    </div>
                    <div>
                      <span className="text-gray-400">Tire Degradation:</span>
                      <span className={`ml-2 font-medium ${getDifficultyColor(result.track_conditions.tire_degradation)}`}>
                        {result.track_conditions.tire_degradation.toFixed(0)}%
                      </span>
                    </div>
                    <div>
                      <span className="text-gray-400">Overtaking Difficulty:</span>
                      <span className={`ml-2 font-medium ${getDifficultyColor(result.track_conditions.overtaking_difficulty)}`}>
                        {result.track_conditions.overtaking_difficulty.toFixed(0)}%
                      </span>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Strategy Comparison */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Optimal Strategy */}
              <div className="bg-gray-700 rounded-lg p-6">
                <h3 className="text-xl font-semibold text-white mb-4">Optimal Strategy</h3>
                
                <div className="space-y-3 mb-4">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Pit Stops:</span>
                    <span className="text-white font-bold">{result.optimal_strategy.stops}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Total Time:</span>
                    <span className="text-white font-bold">{(result.optimal_strategy.total_time / 60).toFixed(2)}m</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Time Penalty:</span>
                    <span className="text-white">{result.optimal_strategy.time_penalty}s</span>
                  </div>
                </div>

                <div className="space-y-2">
                  <p className="text-gray-400 text-sm">Stint Breakdown:</p>
                  {result.optimal_strategy.stints.map((stint, index) => (
                    <div key={index} className="flex items-center justify-between bg-gray-800 rounded p-2">
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded text-xs font-bold text-white ${getTireColor(stint.compound)}`}>
                          {stint.compound}
                        </span>
                        <span className="text-white text-sm">({stint.laps} laps)</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Actual Strategy */}
              <div className="bg-gray-700 rounded-lg p-6">
                <h3 className="text-xl font-semibold text-white mb-4">Actual Strategy</h3>
                
                {result.actual_strategy.error ? (
                  <div className="text-gray-400 text-center py-8">
                    <p>{result.actual_strategy.error}</p>
                  </div>
                ) : (
                  <>
                    <div className="space-y-3 mb-4">
                      <div className="flex justify-between">
                        <span className="text-gray-400">Pit Stops:</span>
                        <span className="text-white font-bold">{result.actual_strategy.stops || 0}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-400">Total Time:</span>
                        <span className="text-white font-bold">
                          {result.actual_strategy.total_time ? 
                            (result.actual_strategy.total_time / 60).toFixed(2) + 'm' : 'N/A'}
                        </span>
                      </div>
                    </div>

                    {result.actual_strategy.stints && (
                      <div className="space-y-2">
                        <p className="text-gray-400 text-sm">Stint Breakdown:</p>
                        {result.actual_strategy.stints.map((stint, index) => (
                          <div key={index} className="flex items-center justify-between bg-gray-800 rounded p-2">
                            <div className="flex items-center space-x-2">
                              <span className={`px-2 py-1 rounded text-xs font-bold text-white ${getTireColor(stint.compound)}`}>
                                {stint.compound}
                              </span>
                              <span className="text-white text-sm">({stint.laps} laps, L{stint.start_lap}-{stint.end_lap})</span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </>
                )}
              </div>
            </div>

            {/* Strategy Analysis */}
            <div className="bg-gray-700 rounded-lg p-6">
              <h3 className="text-xl font-semibold text-white mb-4">Strategy Analysis</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="text-center">
                  <p className="text-gray-400 text-sm">Potential Time Savings</p>
                  <p className={`text-3xl font-bold ${
                    result.time_savings > 0 ? 'text-green-400' : 
                    result.time_savings < -5 ? 'text-red-400' : 'text-yellow-400'
                  }`}>
                    {result.time_savings > 0 ? '+' : ''}{result.time_savings.toFixed(2)}s
                  </p>
                </div>
                
                <div className="text-center">
                  <p className="text-gray-400 text-sm">Available Compounds</p>
                  <div className="flex justify-center space-x-1 mt-2">
                    {result.available_compounds.map((compound) => (
                      <span key={compound} className={`w-6 h-6 rounded ${getTireColor(compound)}`} title={compound}></span>
                    ))}
                  </div>
                </div>
                
                <div className="text-center">
                  <p className="text-gray-400 text-sm">Strategy Effectiveness</p>
                  <p className={`text-2xl font-bold ${
                    result.time_savings > 15 ? 'text-green-400' :
                    result.time_savings > 5 ? 'text-yellow-400' : 
                    result.time_savings > -5 ? 'text-orange-400' : 'text-red-400'
                  }`}>
                    {result.time_savings > 15 ? 'Excellent' :
                     result.time_savings > 5 ? 'Good' : 
                     result.time_savings > -5 ? 'Fair' : 'Poor'}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default StrategyOptimization; 