# 🏎️ F1 Analytics Dashboard

A comprehensive Formula 1 analytics platform featuring race predictions, strategy optimization, driver performance analysis, and championship standings for seasons 2018-2025.

## ✨ Features

- **📊 Dashboard Overview**: Championship standings, race calendar, and key statistics
- **⚡ Strategy Optimization**: AI-powered pit stop strategy analysis
- **🏎️ Driver Analytics**: Individual and comparative driver performance analysis  
- **🎯 Race Predictions**: ML-powered race outcome forecasting
- **🏆 Multi-Season Support**: Complete data for 2018-2025 seasons

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Git** (for cloning)

### Installation & Setup

1. **Clone and enter the project directory:**
   ```bash
   git clone <repository-url>
   cd F1
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies:**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

#### Option 1: Automatic Startup (Recommended)
Run the complete dashboard with one command:
```bash
python start_dashboard.py
```

#### Option 2: Manual Startup (If automatic fails)

**Terminal 1 - Backend API:**
```bash
python start_backend.py
```

**Terminal 2 - Frontend Dashboard:**
```bash
cd frontend
npm start
```

### Access the Application

- **🎯 Dashboard**: http://localhost:3000
- **🔧 API Server**: http://localhost:5000

## 📋 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/races?year=2025` | GET | Race calendar |
| `/api/strategy-optimization` | POST | Strategy analysis |
| `/api/driver-performance/{driver}` | GET | Driver analytics |
| `/api/driver-comparison` | POST | Multi-driver comparison |
| `/api/predict-race` | POST | Race predictions |
| `/api/season-standings/{year}` | GET | Championship standings |

## 🎮 Usage Guide

### Dashboard
- View championship standings for drivers and constructors
- Browse race calendar with results status
- See key statistics and metrics

### Strategy Optimization
1. Select year, race round, and driver
2. Click "Optimize Strategy" 
3. View optimal vs actual pit stop strategies
4. Analyze potential time savings

### Driver Analytics
**Individual Analysis:**
- Select driver and season
- View performance metrics and skill ratings
- Review race-by-race results

**Driver Comparison:**
- Select multiple drivers to compare
- View side-by-side skill analysis
- Compare performance metrics

### Race Predictions
1. Choose season and race
2. Generate ML-powered predictions
3. View winner, podium, and points predictions
4. Analyze probability distributions

## 🛠️ Technical Architecture

### Backend (Python/Flask)
- **FastF1**: Official F1 data processing
- **Flask**: REST API server
- **Pandas/NumPy**: Data analysis
- **Scikit-learn**: Machine learning models

### Frontend (React/TypeScript)
- **React 19**: Modern UI framework
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Styling framework
- **Axios**: API communication

### Key Components
- `app.py`: Main Flask API server
- `data_processor.py`: F1 data handling with 2025 calendar
- `strategy_optimizer.py`: Pit stop strategy algorithms
- `driver_analyzer.py`: Driver performance analysis
- `race_predictor.py`: ML prediction models

## 🎨 Features Breakdown

### Strategy Optimization Algorithm
- Track-specific tire degradation modeling
- Driver skill factor adjustments
- Team car performance considerations
- Realistic compound performance gaps
- Multi-stop strategy evaluation

### Driver Analytics
- Skill ratings: consistency, speed, qualifying, race craft, wet weather, overtaking
- Mock race generation based on driver profiles
- Position gain/loss tracking
- Q3 appearance statistics

### Race Predictions
- Track characteristic adjustments
- Team-specific performance modifiers
- Driver weight calculations
- Probability normalization with variance

## 🗂️ Data Coverage

### Seasons: 2018-2025
- **2025**: Complete projected calendar (24 races)
- **2018-2024**: Historical data support
- **Drivers**: 40+ drivers across all seasons
- **Teams**: All constructor data

### 2025 Season Details
- 24-race calendar from Australia to Abu Dhabi
- Updated driver lineups and team changes
- Lewis Hamilton to Ferrari, Sergio Pérez departure
- New rookies and driver market changes

## 🐛 Troubleshooting

### Common Issues

**Frontend won't start:**
```bash
cd frontend
npm install react-scripts
npm start
```

**Backend import errors:**
```bash
pip install -r requirements.txt
```

**Port conflicts:**
- Backend uses port 5000
- Frontend uses port 3000
- Stop conflicting services if needed

**FastF1 cache issues:**
```bash
# Clear cache directory if needed
rm -rf cache/
```

### Development Mode

Both services run in development mode with:
- **Backend**: Auto-reload on code changes
- **Frontend**: Hot module replacement
- **Debug**: Detailed error logging

## 📊 Data Sources

- **FastF1**: Official Formula 1 timing and telemetry data
- **Custom Models**: Driver skill ratings and track characteristics
- **Projected Data**: 2025 season calendar and mock standings
- **Historical Data**: 2018-2024 race results and statistics

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV=development` (auto-set)
- `REACT_APP_API_URL=http://localhost:5000` (default)

### Cache Management
FastF1 data is cached in `cache/` directory for performance. Cache automatically manages downloads and storage.

## 🏁 Project Status

**Current Status**: ✅ Fully Functional
- All backend services restored and working
- Complete frontend React application
- Full 2018-2025 season support
- ML-powered predictions operational
- Strategy optimization algorithms active

**Recent Updates**:
- Restored complete backend after file loss
- Updated to 2025 season as default
- Enhanced strategy optimization algorithms
- Improved driver filtering and validation
- Added comprehensive error handling

---

**🏆 Ready to race! Fire up your engines and dive into the world of Formula 1 analytics!**
