import React, { useState } from 'react';
import axios from 'axios';
import { getAllDrivers, YEARS } from '../constants/drivers';

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
}

const StrategyOptimization: React.FC = () => {
  const [year, setYear] = useState(2025);
  const [round, setRound] = useState(1);
  const [driver, setDriver] = useState('VER');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<StrategyResult | null>(null);

  const optimizeStrategy = async () => {
    try {
      setLoading(true);
      const response = await axios.post('http://localhost:5000/api/strategy-optimization', {
        year,
        round,
        driver
      });
      
      if (response.data.success) {
        setResult(response.data.data);
      }
    } catch (error) {
      console.error('Error optimizing strategy:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTireColor = (compound: string) => {
    switch (compound.toUpperCase()) {
      case 'SOFT': return 'bg-red-500';
      case 'MEDIUM': return 'bg-yellow-500';
      case 'HARD': return 'bg-white';
      case 'INTERMEDIATE': return 'bg-green-500';
      case 'WET': return 'bg-blue-500';
      default: return 'bg-gray-500';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-white">Strategy Optimization</h2>
        <p className="text-gray-400">Optimize pit stop strategies using race simulation</p>
      </div>

      {/* Input Controls */}
      <div className="f1-card p-6">
        <h3 className="text-xl font-bold text-white mb-4">Race Parameters</h3>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-gray-400 text-sm mb-2">Year</label>
            <select
              value={year}
              onChange={(e) => setYear(Number(e.target.value))}
              className="f1-input w-full"
            >
              {YEARS.map(year => (
                <option key={year} value={year}>
                  {year}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-gray-400 text-sm mb-2">Round</label>
            <select
              value={round}
              onChange={(e) => setRound(Number(e.target.value))}
              className="f1-input w-full"
            >
              {Array.from({ length: 24 }, (_, i) => i + 1).map(roundNum => (
                <option key={roundNum} value={roundNum}>
                  Round {roundNum}
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-gray-400 text-sm mb-2">Driver</label>
            <select
              value={driver}
              onChange={(e) => setDriver(e.target.value)}
              className="f1-input w-full"
            >
              {getAllDrivers().map((driver) => (
                <option key={driver.code} value={driver.code}>
                  {driver.name} ({driver.code})
                </option>
              ))}
            </select>
          </div>
          <div className="flex items-end">
            <button
              onClick={optimizeStrategy}
              disabled={loading}
              className="f1-button w-full disabled:opacity-50"
            >
              {loading ? 'Optimizing...' : 'Optimize Strategy'}
            </button>
          </div>
        </div>
      </div>

      {result && (
        <>
          {/* Strategy Comparison */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="f1-card p-6">
              <h3 className="text-xl font-bold text-white mb-4">Optimal Strategy</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Pit Stops:</span>
                  <span className="text-white font-bold">{result.optimal_strategy.stops}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Total Time:</span>
                  <span className="text-white font-bold">
                    {Math.floor(result.optimal_strategy.total_time / 60)}:
                    {(result.optimal_strategy.total_time % 60).toFixed(2).padStart(5, '0')}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Time Penalty:</span>
                  <span className="text-white font-bold">{result.optimal_strategy.time_penalty}s</span>
                </div>
                
                <div className="space-y-2">
                  <p className="text-gray-400 text-sm">Stint Breakdown:</p>
                  {result.optimal_strategy.stints.map((stint, index) => (
                    <div key={index} className="flex items-center space-x-3">
                      <div className={`w-4 h-4 rounded-full ${getTireColor(stint.compound)}`}></div>
                      <span className="text-white">{stint.compound}</span>
                      <span className="text-gray-400">({stint.laps} laps)</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="f1-card p-6">
              <h3 className="text-xl font-bold text-white mb-4">Actual Strategy</h3>
              {result.actual_strategy.error ? (
                <p className="text-gray-400">{result.actual_strategy.error}</p>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Pit Stops:</span>
                    <span className="text-white font-bold">{result.actual_strategy.stops}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-400">Total Time:</span>
                    <span className="text-white font-bold">
                      {result.actual_strategy.total_time ? 
                        `${Math.floor(result.actual_strategy.total_time / 60)}:${(result.actual_strategy.total_time % 60).toFixed(2).padStart(5, '0')}` : 
                        'N/A'
                      }
                    </span>
                  </div>
                  
                  <div className="space-y-2">
                    <p className="text-gray-400 text-sm">Stint Breakdown:</p>
                    {result.actual_strategy.stints?.map((stint, index) => (
                      <div key={index} className="flex items-center space-x-3">
                        <div className={`w-4 h-4 rounded-full ${getTireColor(stint.compound)}`}></div>
                        <span className="text-white">{stint.compound}</span>
                        <span className="text-gray-400">
                          ({stint.laps} laps, L{stint.start_lap}-{stint.end_lap})
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Time Savings */}
          <div className="f1-card p-6">
            <h3 className="text-xl font-bold text-white mb-4">Strategy Analysis</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <p className="text-gray-400 text-sm">Potential Time Savings</p>
                <p className={`text-3xl font-bold ${result.time_savings > 0 ? 'text-green-400' : 'text-red-400'}`}>
                  {result.time_savings > 0 ? '+' : ''}{result.time_savings.toFixed(2)}s
                </p>
              </div>
              <div className="text-center">
                <p className="text-gray-400 text-sm">Available Compounds</p>
                <div className="flex justify-center space-x-2 mt-2">
                  {result.available_compounds.map((compound) => (
                    <div
                      key={compound}
                      className={`w-6 h-6 rounded-full ${getTireColor(compound)}`}
                      title={compound}
                    ></div>
                  ))}
                </div>
              </div>
              <div className="text-center">
                <p className="text-gray-400 text-sm">Strategy Effectiveness</p>
                <p className="text-3xl font-bold text-white">
                  {result.time_savings > 10 ? 'Excellent' : 
                   result.time_savings > 0 ? 'Good' : 
                   result.time_savings > -10 ? 'Fair' : 'Poor'}
                </p>
              </div>
            </div>
          </div>

          {/* Pit Stop Timing */}
          <div className="f1-card p-6">
            <h3 className="text-xl font-bold text-white mb-4">Pit Stop Timing</h3>
            <div className="space-y-4">
              <div>
                <p className="text-gray-400 text-sm mb-2">Optimal Pit Laps</p>
                <div className="flex space-x-2">
                  {result.optimal_strategy.pit_laps.map((lap, index) => (
                    <span key={index} className="bg-f1-red text-white px-3 py-1 rounded">
                      Lap {lap}
                    </span>
                  ))}
                </div>
              </div>
              {!result.actual_strategy.error && (
                <div>
                  <p className="text-gray-400 text-sm mb-2">Actual Pit Laps</p>
                  <div className="flex space-x-2">
                    {result.actual_strategy.pit_laps?.map((lap, index) => (
                      <span key={index} className="bg-gray-600 text-white px-3 py-1 rounded">
                        Lap {lap}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default StrategyOptimization; 