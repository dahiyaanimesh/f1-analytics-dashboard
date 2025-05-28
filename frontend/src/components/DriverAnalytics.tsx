import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { getDriversForYear, YEARS } from '../constants/drivers';

interface DriverPerformance {
  overall_metrics: {
    average_race_position: number;
    average_qualifying_position: number;
    total_points: number;
    total_positions_gained: number;
    position_consistency: number;
    q3_appearances: number;
    races_completed: number;
    total_races: number;
  };
  skill_ratings: {
    consistency: number;
    speed: number;
    qualifying_performance: number;
    race_craft: number;
    wet_weather: number;
    overtaking: number;
  };
  races: Array<{
    race_name: string;
    position: number;
    grid_position: number;
    positions_gained: number;
    points: number;
  }>;
}

interface ComparisonData {
  drivers: string[];
  metrics_comparison: {
    [key: string]: { [driver: string]: number };
  };
  skill_ratings: {
    [key: string]: { [driver: string]: number };
  };
}

const DriverAnalytics: React.FC = () => {
  const [selectedDriver, setSelectedDriver] = useState('VER');
  const [selectedYear, setSelectedYear] = useState(2025);
  const [comparisonDrivers, setComparisonDrivers] = useState<string[]>(['VER', 'LEC']);
  const [driverData, setDriverData] = useState<DriverPerformance | null>(null);
  const [comparisonData, setComparisonData] = useState<ComparisonData | null>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('individual');

  // Filter drivers for the selected year
  const availableDrivers = getDriversForYear(selectedYear);
  
  // Ensure selected driver is valid for the current year
  useEffect(() => {
    if (!availableDrivers.find(d => d.code === selectedDriver)) {
      if (availableDrivers.length > 0) {
        setSelectedDriver(availableDrivers[0].code);
      }
    }
  }, [selectedYear, availableDrivers, selectedDriver]);
  
  // Filter comparison drivers to only include those valid for the selected year
  useEffect(() => {
    const validDrivers = comparisonDrivers.filter(driver => 
      availableDrivers.find(d => d.code === driver)
    );
    if (validDrivers.length !== comparisonDrivers.length) {
      setComparisonDrivers(validDrivers);
    }
  }, [selectedYear, availableDrivers, comparisonDrivers]);

  const analyzeDriver = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:5000/api/driver-performance/${selectedDriver}?year=${selectedYear}`);
      
      if (response.data.success) {
        setDriverData(response.data.data);
      }
    } catch (error) {
      console.error('Error analyzing driver:', error);
    } finally {
      setLoading(false);
    }
  };

  const compareDrivers = async () => {
    try {
      setLoading(true);
      const response = await axios.post('http://localhost:5000/api/driver-comparison', {
        drivers: comparisonDrivers,
        year: selectedYear
      });
      
      if (response.data.success) {
        setComparisonData(response.data.data);
      }
    } catch (error) {
      console.error('Error comparing drivers:', error);
    } finally {
      setLoading(false);
    }
  };

  const getSkillColor = (rating: number) => {
    if (rating >= 80) return 'bg-green-500';
    if (rating >= 60) return 'bg-yellow-500';
    if (rating >= 40) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const renderSkillBar = (skill: string, rating: number) => (
    <div key={skill} className="space-y-2">
      <div className="flex justify-between">
        <span className="text-gray-300 capitalize">{skill.replace('_', ' ')}</span>
        <span className="text-white font-bold">{rating.toFixed(0)}</span>
      </div>
      <div className="w-full bg-gray-700 rounded-full h-2">
        <div
          className={`h-2 rounded-full ${getSkillColor(rating)}`}
          style={{ width: `${rating}%` }}
        ></div>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-white">Driver Analytics</h2>
        <div className="flex space-x-2">
          <button
            onClick={() => setActiveTab('individual')}
            className={`px-4 py-2 rounded ${activeTab === 'individual' ? 'bg-f1-red text-white' : 'bg-gray-600 text-gray-300'}`}
          >
            Individual Analysis
          </button>
          <button
            onClick={() => setActiveTab('comparison')}
            className={`px-4 py-2 rounded ${activeTab === 'comparison' ? 'bg-f1-red text-white' : 'bg-gray-600 text-gray-300'}`}
          >
            Driver Comparison
          </button>
        </div>
      </div>

      {activeTab === 'individual' && (
        <>
          {/* Individual Driver Analysis Controls */}
          <div className="f1-card p-6">
            <h3 className="text-xl font-bold text-white mb-4">Driver Selection</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-gray-400 text-sm mb-2">
                  Driver ({availableDrivers.length} available in {selectedYear})
                </label>
                <select
                  value={selectedDriver}
                  onChange={(e) => setSelectedDriver(e.target.value)}
                  className="f1-input w-full"
                >
                  {availableDrivers.map((driver) => (
                    <option key={driver.code} value={driver.code}>
                      {driver.name} ({driver.code})
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-gray-400 text-sm mb-2">Season</label>
                <select
                  value={selectedYear}
                  onChange={(e) => setSelectedYear(Number(e.target.value))}
                  className="f1-input w-full"
                >
                  {YEARS.map(year => (
                    <option key={year} value={year}>{year}</option>
                  ))}
                </select>
              </div>
              <div className="flex items-end">
                <button
                  onClick={analyzeDriver}
                  disabled={loading}
                  className="f1-button w-full disabled:opacity-50"
                >
                  {loading ? 'Analyzing...' : 'Analyze Driver'}
                </button>
              </div>
            </div>
          </div>

          {driverData && (
            <>
              {/* Performance Metrics */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="f1-card p-6 text-center">
                  <p className="text-gray-400 text-sm">Average Position</p>
                  <p className="text-3xl font-bold text-white">
                    {driverData.overall_metrics.average_race_position.toFixed(1)}
                  </p>
                </div>
                <div className="f1-card p-6 text-center">
                  <p className="text-gray-400 text-sm">Total Points</p>
                  <p className="text-3xl font-bold text-f1-gold">
                    {driverData.overall_metrics.total_points}
                  </p>
                </div>
                <div className="f1-card p-6 text-center">
                  <p className="text-gray-400 text-sm">Positions Gained</p>
                  <p className={`text-3xl font-bold ${
                    driverData.overall_metrics.total_positions_gained > 0 ? 'text-green-400' : 'text-red-400'
                  }`}>
                    {driverData.overall_metrics.total_positions_gained > 0 ? '+' : ''}
                    {driverData.overall_metrics.total_positions_gained}
                  </p>
                </div>
                <div className="f1-card p-6 text-center">
                  <p className="text-gray-400 text-sm">Q3 Appearances</p>
                  <p className="text-3xl font-bold text-white">
                    {driverData.overall_metrics.q3_appearances}
                  </p>
                </div>
              </div>

              {/* Skill Ratings */}
              <div className="f1-card p-6">
                <h3 className="text-xl font-bold text-white mb-6">Skill Ratings</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {Object.entries(driverData.skill_ratings).map(([skill, rating]) =>
                    renderSkillBar(skill, rating)
                  )}
                </div>
              </div>

              {/* Recent Race Results */}
              <div className="f1-card p-6">
                <h3 className="text-xl font-bold text-white mb-4">Race Results</h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead>
                      <tr className="border-b border-gray-600">
                        <th className="text-gray-400 font-semibold pb-2">Race</th>
                        <th className="text-gray-400 font-semibold pb-2">Grid</th>
                        <th className="text-gray-400 font-semibold pb-2">Finish</th>
                        <th className="text-gray-400 font-semibold pb-2">+/-</th>
                        <th className="text-gray-400 font-semibold pb-2">Points</th>
                      </tr>
                    </thead>
                    <tbody>
                      {driverData.races.slice(0, 10).map((race, index) => (
                        <tr key={index} className="border-b border-gray-700">
                          <td className="py-3 text-white">{race.race_name}</td>
                          <td className="py-3 text-gray-300">{race.grid_position}</td>
                          <td className="py-3 text-white font-semibold">{race.position}</td>
                          <td className={`py-3 font-semibold ${
                            race.positions_gained > 0 ? 'text-green-400' : 
                            race.positions_gained < 0 ? 'text-red-400' : 'text-gray-400'
                          }`}>
                            {race.positions_gained > 0 ? '+' : ''}{race.positions_gained}
                          </td>
                          <td className="py-3 text-f1-gold font-bold">{race.points}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </>
          )}
        </>
      )}

      {activeTab === 'comparison' && (
        <>
          {/* Driver Comparison Controls */}
          <div className="f1-card p-6">
            <h3 className="text-xl font-bold text-white mb-4">Driver Comparison</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-gray-400 text-sm mb-2">
                  Drivers to Compare ({availableDrivers.length} available in {selectedYear})
                </label>
                <div className="grid grid-cols-2 gap-2 max-h-48 overflow-y-auto">
                  {availableDrivers.slice(0, 20).map((driver) => (
                    <label key={driver.code} className="flex items-center space-x-2">
                      <input
                        type="checkbox"
                        checked={comparisonDrivers.includes(driver.code)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setComparisonDrivers([...comparisonDrivers, driver.code]);
                          } else {
                            setComparisonDrivers(comparisonDrivers.filter(d => d !== driver.code));
                          }
                        }}
                        className="rounded"
                      />
                      <span className="text-white text-sm">{driver.name}</span>
                    </label>
                  ))}
                </div>
              </div>
              <div>
                <label className="block text-gray-400 text-sm mb-2">Season</label>
                <select
                  value={selectedYear}
                  onChange={(e) => setSelectedYear(Number(e.target.value))}
                  className="f1-input w-full"
                >
                  {YEARS.map(year => (
                    <option key={year} value={year}>{year}</option>
                  ))}
                </select>
              </div>
              <div className="flex items-end">
                <button
                  onClick={compareDrivers}
                  disabled={loading || comparisonDrivers.length < 2}
                  className="f1-button w-full disabled:opacity-50"
                >
                  {loading ? 'Comparing...' : 'Compare Drivers'}
                </button>
              </div>
            </div>
          </div>

          {comparisonData && (
            <div className="f1-card p-6">
              <h3 className="text-xl font-bold text-white mb-6">Skill Comparison</h3>
              <div className="space-y-6">
                {Object.entries(comparisonData.skill_ratings).map(([skill, drivers]) => (
                  <div key={skill} className="space-y-2">
                    <h4 className="text-white font-semibold capitalize">
                      {skill.replace('_', ' ')}
                    </h4>
                    <div className="space-y-1">
                      {Object.entries(drivers).map(([driver, rating]) => (
                        <div key={driver} className="flex items-center space-x-3">
                          <span className="text-gray-400 w-12">{driver}</span>
                          <div className="flex-1 bg-gray-700 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full ${getSkillColor(rating)}`}
                              style={{ width: `${rating}%` }}
                            ></div>
                          </div>
                          <span className="text-white font-bold w-12">
                            {rating.toFixed(0)}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {loading && (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-f1-red"></div>
        </div>
      )}
    </div>
  );
};

export default DriverAnalytics; 