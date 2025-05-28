import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-f1-dark border-b border-gray-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <div className="f1-gradient w-10 h-10 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-xl">F1</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">F1 Analytics Dashboard</h1>
            <p className="text-gray-400 text-sm">Real-time Formula 1 data insights</p>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          <div className="text-sm text-gray-400">
            Season 2023 • Live Data
          </div>
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
        </div>
      </div>
    </header>
  );
};

export default Header; 