#!/usr/bin/env python3
"""
F1 Analytics Dashboard Launcher
Starts both backend API and frontend React application
"""

import os
import sys
import time
import subprocess
import threading
import signal
from pathlib import Path

class F1DashboardLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        
    def print_f1_banner(self):
        """Print F1-themed startup banner"""
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          🏎️  F1 ANALYTICS DASHBOARD  🏎️                         ║
║                                                                              ║
║                    🏁 Starting your Formula 1 analytics experience! 🏁        ║
╚══════════════════════════════════════════════════════════════════════════════╝

🔧 Initializing race control systems...
📊 Loading telemetry data processors...
🏆 Preparing championship standings...
⚡ Optimizing pit stop strategies...
🎯 Calibrating race prediction models...
"""
        print(banner)
        
    def check_dependencies(self):
        """Check if required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        # Check Python dependencies
        try:
            import flask
            import pandas
            import numpy
            import fastf1
            print("✅ Backend dependencies: OK")
        except ImportError as e:
            print(f"❌ Missing Python dependency: {e}")
            print("📦 Installing backend dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        # Check if Node.js is available
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Node.js: {result.stdout.strip()}")
            else:
                print("❌ Node.js not found")
                return False
        except FileNotFoundError:
            print("❌ Node.js not found. Please install Node.js to run the frontend.")
            return False
        
        # Check if npm dependencies are installed
        frontend_path = Path("frontend")
        if frontend_path.exists():
            node_modules = frontend_path / "node_modules"
            if not node_modules.exists():
                print("📦 Installing frontend dependencies...")
                subprocess.run(["npm", "install"], cwd=frontend_path)
        
        return True
    
    def start_backend(self):
        """Start the Flask backend server"""
        print("\n🚀 Starting F1 Analytics API server...")
        print("🔗 Backend URL: http://localhost:5000")
        
        try:
            # Start Flask app
            self.backend_process = subprocess.Popen(
                [sys.executable, "app.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give the backend a moment to start
            time.sleep(2)
            
            if self.backend_process.poll() is None:
                print("✅ Backend server started successfully!")
            else:
                print("❌ Backend server failed to start")
                stdout, stderr = self.backend_process.communicate()
                print(f"Error: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
        
        return True
    
    def start_frontend(self):
        """Start the React frontend development server"""
        print("\n🎨 Starting F1 Dashboard frontend...")
        print("🔗 Frontend URL: http://localhost:3000")
        
        frontend_path = Path("frontend")
        if not frontend_path.exists():
            print("❌ Frontend directory not found")
            return False
        
        try:
            # Start React development server
            self.frontend_process = subprocess.Popen(
                ["npm", "start"],
                cwd=frontend_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give the frontend time to start
            time.sleep(3)
            
            if self.frontend_process.poll() is None:
                print("✅ Frontend server started successfully!")
            else:
                print("❌ Frontend server failed to start")
                stdout, stderr = self.frontend_process.communicate()
                print(f"Error: {stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting frontend: {e}")
            return False
        
        return True
    
    def monitor_processes(self):
        """Monitor both processes and restart if needed"""
        while self.running:
            time.sleep(5)
            
            # Check backend
            if self.backend_process and self.backend_process.poll() is not None:
                print("⚠️  Backend process stopped unexpectedly")
                break
            
            # Check frontend
            if self.frontend_process and self.frontend_process.poll() is not None:
                print("⚠️  Frontend process stopped unexpectedly")
                break
    
    def print_startup_complete(self):
        """Print completion message with access URLs"""
        completion_message = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                            🏎️  SYSTEMS ONLINE!  🏎️                            ║
║                                                                              ║
║  🎯 Dashboard:    http://localhost:3000                                      ║
║  🔧 API Server:   http://localhost:5000                                      ║
║                                                                              ║
║  📊 Available Features:                                                      ║
║     • Race Predictions & Analytics                                           ║
║     • Driver Performance Comparisons                                         ║
║     • Pit Stop Strategy Optimization                                         ║
║     • Championship Standings (2018-2025)                                     ║
║                                                                              ║
║  🏁 Ready for racing! Press Ctrl+C to stop all services.                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        print(completion_message)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print("\n\n🛑 Shutting down F1 Analytics Dashboard...")
        self.shutdown()
    
    def shutdown(self):
        """Gracefully shutdown both servers"""
        self.running = False
        
        if self.frontend_process:
            print("🔌 Stopping frontend server...")
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
        
        if self.backend_process:
            print("🔌 Stopping backend server...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
        
        print("🏁 All services stopped. Thanks for using F1 Analytics Dashboard!")
        sys.exit(0)
    
    def run(self):
        """Main execution method"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Print banner
        self.print_f1_banner()
        
        # Check dependencies
        if not self.check_dependencies():
            print("❌ Dependency check failed. Please install required dependencies.")
            return
        
        # Start backend
        if not self.start_backend():
            print("❌ Failed to start backend server")
            return
        
        # Start frontend
        if not self.start_frontend():
            print("❌ Failed to start frontend server")
            self.shutdown()
            return
        
        # Print completion message
        self.print_startup_complete()
        
        # Monitor processes
        try:
            self.monitor_processes()
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()

def main():
    """Entry point"""
    launcher = F1DashboardLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 