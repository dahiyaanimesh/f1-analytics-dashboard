# 🏎️ F1 Analytics Dashboard

A comprehensive Formula 1 analytics platform that provides advanced race insights, driver performance analysis, strategy optimization, and AI-powered race predictions. Built with React, TypeScript, and Python using real F1 data from the FastF1 library.

![F1 Analytics Dashboard](https://img.shields.io/badge/F1-Analytics%20Dashboard-red?style=for-the-badge&logo=formula1)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-4.9+-blue?style=for-the-badge&logo=typescript)

## ✨ Features

### 🏁 **Dashboard Overview**
- **Season Statistics**: Live championship standings and race calendar
- **Driver & Constructor Championships**: Real-time points tracking
- **Race Results**: Comprehensive race outcome analysis
- **Season Coverage**: 2018-2025 seasons supported

### 🏃‍♂️ **Driver Analytics**
- **Individual Performance Analysis**: Detailed driver metrics and skill ratings
- **Multi-Driver Comparison**: Side-by-side performance comparison
- **Skill Ratings**: Consistency, speed, qualifying performance, race craft, wet weather, and overtaking
- **Race Results Tracking**: Grid positions, finishing positions, and points progression
- **Season-Specific Filtering**: Drivers automatically filtered by active seasons

### 🎯 **Strategy Optimization**
- **Pit Stop Strategy Analysis**: Optimal vs actual strategy comparison
- **Tire Performance Modeling**: Realistic compound degradation patterns
- **Driver-Specific Characteristics**: Personalized tire management and pace modeling
- **Team-Based Analytics**: Car-specific tire performance factors
- **Track-Type Adaptation**: Strategy varies by track characteristics
- **Time Savings Calculation**: Quantified strategic improvements

### 🔮 **Race Prediction**
- **AI-Powered Predictions**: Machine learning race outcome forecasts
- **Winner Probability**: Statistical likelihood of race winners
- **Podium Predictions**: Top 8 finish probabilities
- **Points Scoring Chances**: Top 10 finish likelihood analysis
- **Historical Data Training**: Models trained on extensive F1 historical data

## 🛠️ Technology Stack

### **Frontend**
- **React 19** with TypeScript
- **Tailwind CSS** for styling
- **Axios** for API communication
- **Custom F1-themed UI components**

### **Backend**
- **Python 3.8+** with Flask
- **FastF1** library for official F1 data
- **Pandas & NumPy** for data processing
- **Scikit-learn & XGBoost** for ML predictions
- **Plotly** for data visualization
- **SciPy** for optimization algorithms

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**

### 1. Clone the Repository
```bash
git clone <repository-url>
cd f1-analytics-dashboard
```

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the Flask backend
python start_dashboard.py
```
The backend will be available at `http://localhost:5000`

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```
The frontend will be available at `http://localhost:3000`

## 📁 Project Structure

```
F1/
├── 📁 frontend/                  # React TypeScript frontend
│   ├── 📁 public/               # Static assets
│   │   ├── 📁 components/       # React components
│   │   │   ├── Dashboard.tsx    # Main dashboard
│   │   │   ├── DriverAnalytics.tsx
│   │   │   ├── StrategyOptimization.tsx
│   │   │   ├── RacePrediction.tsx
│   │   │   ├── Header.tsx
│   │   │   └── Sidebar.tsx
│   │   ├── 📁 constants/        # Shared constants
│   │   │   └── drivers.ts       # Driver database (2018-2025)
│   │   └── 📁 styles/          # Tailwind CSS
│   └── package.json
├── 📁 cache/                    # FastF1 data cache
│   ├── 📁 2021/                # Historical season data
│   ├── 📁 2023/
│   ├── 📁 2024/
│   └── 📁 2025/
├── app.py                       # Flask API endpoints
├── data_processor.py            # F1 data processing
├── driver_analyzer.py           # Driver performance analysis
├── race_predictor.py            # ML race predictions
├── strategy_optimizer.py        # Pit stop optimization
├── start_dashboard.py           # Application launcher
├── requirements.txt             # Python dependencies
└── README.md
```

## 🔧 Configuration

### **Driver Database**
The system includes a comprehensive driver database covering 2018-2025:
- **47 drivers total** with season-specific filtering
- **Current 2025 grid** (21 active drivers)
- **Historical drivers** (26 former drivers)
- **Team associations** and season availability

### **Season Coverage**
- **2018-2024**: Historical data via FastF1
- **2025**: Projected season with realistic race calendar
- **Automatic data caching** for improved performance

### **API Endpoints**
```
GET  /api/health                 # Health check
GET  /api/races?year=2025        # Race calendar
GET  /api/race-data/{year}/{round} # Detailed race data
POST /api/strategy-optimization  # Strategy analysis
GET  /api/driver-performance/{driver} # Driver metrics
POST /api/driver-comparison      # Multi-driver analysis
POST /api/predict-race          # Race predictions
GET  /api/season-standings/{year} # Championship standings
```

## 📊 Analytics Features

### **Strategy Optimization Algorithm**
- **Track-Specific Modeling**: Different tire degradation by circuit type
- **Driver Characteristics**: Individual tire management skills
- **Team Car Performance**: Vehicle-specific tire friendliness
- **Weather Adaptation**: Intermediate and wet tire strategies
- **Realistic Pit Times**: Team-specific pit stop efficiency

### **Race Prediction Models**
- **Historical Pattern Analysis**: Multi-season training data
- **Driver Form Weighting**: Recent performance trends
- **Track-Specific Factors**: Circuit characteristics impact
- **Team Performance Trends**: Constructor competitiveness
- **Qualifying Impact**: Grid position influence on race outcome

### **Driver Analytics Metrics**
- **Consistency Rating**: Performance variance analysis
- **Speed Index**: Raw pace assessment
- **Qualifying Performance**: Grid position optimization
- **Race Craft**: Overtaking and defensive capabilities
- **Wet Weather Skill**: Rain performance rating
- **Position Gain/Loss Tracking**: Race-day progression analysis

## 🎨 UI/UX Features

### **F1-Themed Design**
- **Dark Theme**: Professional Formula 1 aesthetic
- **Responsive Layout**: Mobile and desktop optimized
- **Interactive Components**: Dynamic data visualization
- **Real-time Updates**: Live data integration
- **Accessibility**: Screen reader compatible

### **User Experience**
- **Season-Specific Filtering**: Automatic driver/race filtering
- **Smart Defaults**: Intelligent form pre-population
- **Error Handling**: Graceful fallbacks for missing data
- **Loading States**: Professional loading indicators
- **Data Validation**: Input sanitization and validation

## 🔮 Future Enhancements

### **Planned Features**
- [ ] **Live Race Tracking**: Real-time race monitoring
- [ ] **Weather Integration**: Meteorological data impact
- [ ] **Telemetry Analysis**: Car performance deep-dive
- [ ] **Fantasy F1 Integration**: Team management features
- [ ] **Mobile App**: Native iOS/Android applications
- [ ] **Social Features**: Community predictions and discussions

### **Technical Roadmap**
- [ ] **Database Integration**: PostgreSQL/MongoDB for data persistence
- [ ] **Authentication System**: User accounts and preferences
- [ ] **API Rate Limiting**: Enhanced backend performance
- [ ] **Docker Containerization**: Simplified deployment
- [ ] **CI/CD Pipeline**: Automated testing and deployment
- [ ] **Performance Monitoring**: Application analytics

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### **Code Standards**
- **TypeScript**: Strict type checking enabled
- **ESLint**: Code quality enforcement
- **Prettier**: Consistent code formatting
- **React Hooks**: Proper dependency management
- **Python PEP 8**: Style guide compliance

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastF1 Library**: Official F1 data access
- **Formula 1**: Inspiration and data source
- **React Community**: Framework and ecosystem
- **Python Data Science**: Analytics libraries
- **Tailwind CSS**: UI framework

---

**Built with ❤️ for Formula 1 fans and data enthusiasts**

[![GitHub stars](https://img.shields.io/github/stars/dahiyaanimesh/f1-analytics-dashboard?style=social)](https://github.com/dahiyaanimesh/f1-analytics-dashboard/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/dahiyaanimesh/f1-analytics-dashboard?style=social)](https://github.com/dahiyaanimesh/f1-analytics-dashboard/network/members)
[![GitHub issues](https://img.shields.io/github/issues/dahiyaanimesh/f1-analytics-dashboard)](https://github.com/dahiyaanimesh/f1-analytics-dashboard/issues) 
