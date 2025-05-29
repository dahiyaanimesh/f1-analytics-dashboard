#!/usr/bin/env python3
"""
Simple Backend Startup Script for F1 Analytics Dashboard
"""

if __name__ == "__main__":
    print("🚀 Starting F1 Analytics Backend API...")
    print("🔗 Backend URL: http://localhost:5000")
    print("📊 API endpoints available:")
    print("   • /api/health - Health check")
    print("   • /api/races - Race calendar")
    print("   • /api/strategy-optimization - Strategy analysis")
    print("   • /api/driver-performance - Driver analytics")
    print("   • /api/predict-race - Race predictions")
    print("   • /api/season-standings - Championship standings")
    print("\n🏁 Press Ctrl+C to stop the server")
    print("="*60)
    
    # Import and run the Flask app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000) 