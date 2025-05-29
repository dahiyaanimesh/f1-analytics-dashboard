#!/usr/bin/env python3
"""
Start only the F1 Analytics Backend API with visible logs
Perfect for debugging API issues
"""

import subprocess
import sys
import signal
import os

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n🛑 Shutting down F1 Analytics API...")
    sys.exit(0)

def main():
    """Start the backend API server"""
    print("""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                      🏎️  F1 ANALYTICS API SERVER  🏎️                          ║
║                            Backend Only Mode                                  ║
╚═══════════════════════════════════════════════════════════════════════════════╝

🚀 Starting F1 Analytics API server...
🔗 API URL: http://localhost:5000
📋 All logs will appear below:

""")
    
    # Setup signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start Flask app with logs visible in this console
        if os.name == 'nt':  # Windows
            subprocess.run([sys.executable, "app.py"], shell=True)
        else:  # Unix/Linux/Mac
            subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 API server stopped by user")
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 