# 🏎️ F1 Analytics Dashboard

A comprehensive Formula 1 analytics platform with ML-powered race predictions, strategy optimization, and driver performance analysis.

## ✨ Features

- **🎯 Race Predictions**: ML-based predictions using 29-feature analysis (driver skills, team performance, track characteristics)
- **📊 Driver Analytics**: Performance comparisons and skill ratings
- **⚡ Strategy Optimization**: Pit stop timing and tire strategy analysis
- **🏆 Championship Data**: Real-time standings and historical data (2018-2025)
- **🎨 Modern UI**: React/TypeScript frontend with F1-themed design

## 📸 Dashboard Preview

![F1 Analytics Dashboard](https://github.com/dahiyaanimesh/f1-analytics-dashboard/blob/master/frontend/public/home.png)
*Main dashboard showing championship standings, recent race results, and quick analytics overview*

## 🚀 Quick Start

### Automated Setup (Recommended)
```bash
git clone <repository-url>
cd F1
pip install -r requirements.txt
python start_dashboard.py
```

Access the dashboard at [http://localhost:3000](http://localhost:3000)

### Manual Setup
```bash
# Backend
pip install -r requirements.txt
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm start
```

## 📡 API Endpoints

- `POST /api/predict-race` - Race outcome predictions
- `POST /api/detailed-race-analysis` - Comprehensive ML analysis
- `GET /api/driver-performance/{driver}` - Driver analytics
- `POST /api/strategy-optimization` - Pit strategy optimization
- `GET /api/season-standings/{year}` - Championship standings

## 🧠 ML Prediction Features

- **Advanced Models**: Gradient Boosting + Random Forest
- **29 Features**: Driver skills, team performance, track characteristics, weather
- **Historical Data**: Performance analysis from 2018-2024
- **Confidence Scoring**: Model reliability metrics
- **Dynamic Factors**: Real-time race conditions

## 🛠️ Tech Stack

- **Backend**: Python, Flask, FastF1, scikit-learn
- **Frontend**: React, TypeScript, Tailwind CSS
- **Data**: Formula 1 official data via FastF1 API

## 📊 Prediction Accuracy

- 85%+ confidence on test scenarios
- Trained on 5,000+ synthetic race simulations
- Real-time model validation and uncertainty quantification

## 🏁 Project Structure

```
F1/
├── Backend/
│   ├── app.py              # Main API server
│   ├── race_predictor.py   # ML prediction engine
│   ├── driver_analyzer.py  # Driver performance analysis
│   ├── strategy_optimizer.py # Pit strategy optimization
│   └── data_processor.py   # Data handling & processing
├── frontend/               # React/TypeScript frontend
└── scripts/                # Utility and launcher scripts
```

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with ❤️ for Formula 1 enthusiasts and data science lovers.**
