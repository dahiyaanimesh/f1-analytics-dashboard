import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface RaceData {
  round: number;
  name: string;
  location: string;
  country: string;
  date: string;
}

interface StandingsData {
  drivers: Array<{
    driver: string;
    name: string;
    team: string;
    points: number;
  }>;
  constructors: Array<{
    team: string;
    points: number;
  }>;
}

const Dashboard: React.FC = () => {
  const [races, setRaces] = useState<RaceData[]>([]);
  const [standings, setStandings] = useState<StandingsData>({ drivers: [], constructors: [] });
  const [loading, setLoading] = useState(true);
  const [selectedYear] = useState(2025);

  useEffect(() => {
    fetchDashboardData();
  }, [selectedYear]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch races
      const racesResponse = await axios.get(`http://localhost:5000/api/races?year=${selectedYear}`);
      if (racesResponse.data.success) {
        setRaces(racesResponse.data.data);
      }

      // Fetch standings
      const standingsResponse = await axios.get(`http://localhost:5000/api/season-standings/${selectedYear}`);
      if (standingsResponse.data.success) {
        setStandings(standingsResponse.data.data);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-f1-red"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold text-white">F1 Analytics Dashboard</h2>
        <div className="text-sm text-gray-400">
          Last updated: {new Date().toLocaleString()}
        </div>
      </div>

      {/* Key Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="f1-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Total Races</p>
              <p className="text-2xl font-bold text-white">{races.length}</p>
            </div>
            <div className="text-3xl">🏁</div>
          </div>
        </div>

        <div className="f1-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Active Drivers</p>
              <p className="text-2xl font-bold text-white">{standings.drivers.length}</p>
            </div>
            <div className="text-3xl">👤</div>
          </div>
        </div>

        <div className="f1-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Teams</p>
              <p className="text-2xl font-bold text-white">{standings.constructors.length}</p>
            </div>
            <div className="text-3xl">🏎️</div>
          </div>
        </div>

        <div className="f1-card p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-400 text-sm">Season</p>
              <p className="text-2xl font-bold text-white">{selectedYear}</p>
            </div>
            <div className="text-3xl">🏆</div>
          </div>
        </div>
      </div>

      {/* Championship Standings */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="f1-card p-6">
          <h3 className="text-xl font-bold text-white mb-4">Driver Championship</h3>
          <div className="space-y-3">
            {standings.drivers.slice(0, 10).map((driver, index) => (
              <div key={driver.driver} className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-gray-400 w-6">{index + 1}</span>
                  <div>
                    <p className="text-white font-semibold">{driver.name || driver.driver}</p>
                    <p className="text-gray-400 text-sm">{driver.team}</p>
                  </div>
                </div>
                <span className="text-f1-gold font-bold">{driver.points}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="f1-card p-6">
          <h3 className="text-xl font-bold text-white mb-4">Constructor Championship</h3>
          <div className="space-y-3">
            {standings.constructors.slice(0, 10).map((constructor, index) => (
              <div key={constructor.team} className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <span className="text-gray-400 w-6">{index + 1}</span>
                  <p className="text-white font-semibold">{constructor.team}</p>
                </div>
                <span className="text-f1-gold font-bold">{constructor.points}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recent Races */}
      <div className="f1-card p-6">
        <h3 className="text-xl font-bold text-white mb-4">Race Calendar</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-gray-600">
                <th className="text-gray-400 font-semibold pb-2">Round</th>
                <th className="text-gray-400 font-semibold pb-2">Race</th>
                <th className="text-gray-400 font-semibold pb-2">Location</th>
                <th className="text-gray-400 font-semibold pb-2">Date</th>
                <th className="text-gray-400 font-semibold pb-2">Status</th>
              </tr>
            </thead>
            <tbody>
              {races.slice(0, 8).map((race) => (
                <tr key={race.round} className="border-b border-gray-700">
                  <td className="py-3 text-white">{race.round}</td>
                  <td className="py-3 text-white font-semibold">{race.name}</td>
                  <td className="py-3 text-gray-300">{race.location}, {race.country}</td>
                  <td className="py-3 text-gray-300">{race.date}</td>
                  <td className="py-3">
                    <span className="px-2 py-1 bg-green-600 text-white text-xs rounded">
                      Completed
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;