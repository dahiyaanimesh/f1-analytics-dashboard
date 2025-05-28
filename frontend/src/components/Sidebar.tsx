import React from 'react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      icon: '📊',
      description: 'Overview & Statistics'
    },
    {
      id: 'strategy',
      label: 'Strategy Optimization',
      icon: '🏎️',
      description: 'Pit Stop & Race Strategy'
    },
    {
      id: 'drivers',
      label: 'Driver Analytics',
      icon: '👤',
      description: 'Performance Analysis'
    },
    {
      id: 'predictions',
      label: 'Race Predictions',
      icon: '🔮',
      description: 'ML-Powered Forecasts'
    }
  ];

  return (
    <aside className="w-64 bg-f1-gray border-r border-gray-700 min-h-screen">
      <nav className="p-4">
        <div className="space-y-2">
          {menuItems.map((item) => (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full text-left p-3 rounded-lg transition-all duration-200 ${
                activeTab === item.id
                  ? 'bg-f1-red text-white shadow-lg'
                  : 'text-gray-300 hover:bg-gray-600 hover:text-white'
              }`}
            >
              <div className="flex items-center space-x-3">
                <span className="text-xl">{item.icon}</span>
                <div>
                  <div className="font-semibold">{item.label}</div>
                  <div className="text-xs opacity-75">{item.description}</div>
                </div>
              </div>
            </button>
          ))}
        </div>
      </nav>
    </aside>
  );
};

export default Sidebar; 