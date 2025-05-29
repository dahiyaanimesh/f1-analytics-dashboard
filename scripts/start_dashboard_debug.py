#!/usr/bin/env python3
"""
F1 Analytics Dashboard Launcher - Debug Version
Shows all backend and frontend logs in the console
"""

import subprocess
import sys
import time
import os
import signal
import threading
from pathlib import Path

class F1DashboardDebugLauncher:
    """Launch F1 Analytics Dashboard with visible logs"""
    
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True
        self.is_windows = os.name == 'nt'

    def print_banner(self):
        """Print F1 Analytics banner"""
        banner = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    🏎️  F1 ANALYTICS DASHBOARD - DEBUG MODE 🏎️                  ║
║                              Real-time Racing Insights                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""
        print(banner)

    def start_backend(self):
        """Start the Flask backend server with visible logs"""
        print("\n🚀 Starting F1 Analytics API server...")
        print("🔗 Backend URL: http://localhost:5000")
        print("📋 Backend logs will appear below:\n")
        
        try:
            # Start Flask app with logs visible
            if self.is_windows:
                self.backend_process = subprocess.Popen(
                    [sys.executable, "app.py"],
                    shell=True
                )
            else:
                self.backend_process = subprocess.Popen(
                    [sys.executable, "app.py"]
                )
            
            # Give the backend a moment to start
            time.sleep(2)
            
            if self.backend_process.poll() is None:
                print("✅ Backend server started successfully!")
                return True
            else:
                print("❌ Backend server failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False

    def start_frontend_in_new_window(self):
        """Start frontend in a new console window"""
        print("\n🎨 Starting F1 Dashboard frontend in new window...")
        print("🔗 Frontend URL: http://localhost:3000")
        
        frontend_path = Path("frontend")
        if not frontend_path.exists():
            print("❌ Frontend directory not found")
            return False
        
        try:
            if self.is_windows:
                # Start in new command prompt window
                cmd = f'start "F1 Dashboard Frontend" cmd /k "cd /d {frontend_path.absolute()} && npm start"'
                self.frontend_process = subprocess.Popen(cmd, shell=True)
            else:
                # Start in new terminal (varies by system)
                try:
                    # Try gnome-terminal first
                    self.frontend_process = subprocess.Popen([
                        "gnome-terminal", "--", "bash", "-c", 
                        f"cd {frontend_path.absolute()} && npm start; exec bash"
                    ])
                except FileNotFoundError:
                    try:
                        # Try xterm
                        self.frontend_process = subprocess.Popen([
                            "xterm", "-e", f"cd {frontend_path.absolute()} && npm start"
                        ])
                    except FileNotFoundError:
                        # Fall back to same terminal
                        print("⚠️  Could not open new terminal, starting in background...")
                        self.frontend_process = subprocess.Popen(
                            ["npm", "start"], cwd=frontend_path
                        )
            
            time.sleep(3)
            print("✅ Frontend server started in new window!")
            return True
            
        except Exception as e:
            print(f"❌ Error starting frontend: {e}")
            return False

    def monitor_backend(self):
        """Monitor backend process"""
        while self.running:
            if self.backend_process and self.backend_process.poll() is not None:
                print("\n⚠️  Backend process stopped unexpectedly")
                break
            time.sleep(2)

    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print("\n\n🛑 Shutting down F1 Analytics Dashboard...")
        self.shutdown()

    def shutdown(self):
        """Gracefully shutdown both servers"""
        self.running = False
        
        if self.backend_process:
            print("🔌 Stopping backend server...")
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
        
        if self.frontend_process:
            print("🔌 Stopping frontend server...")
            if self.is_windows:
                # On Windows, kill the process tree
                try:
                    subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.frontend_process.pid)], 
                                 shell=True, capture_output=True)
                except:
                    pass
            else:
                self.frontend_process.terminate()
        
        print("🏁 All services stopped. Thanks for using F1 Analytics Dashboard!")
        sys.exit(0)

    def run(self):
        """Main execution method"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Print banner
        self.print_banner()
        
        # Start backend (shows logs in this console)
        if not self.start_backend():
            print("❌ Failed to start backend server")
            return
        
        # Start frontend in new window
        if not self.start_frontend_in_new_window():
            print("❌ Failed to start frontend server")
            self.shutdown()
            return
        
        print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                            🏎️  SYSTEMS ONLINE!  🏎️                            ║
║                                                                              ║
║  🎯 Dashboard:    http://localhost:3000  (separate window)                  ║
║  🔧 API Server:   http://localhost:5000  (logs below)                       ║
║                                                                              ║
║  📊 Backend API logs will appear in this console                            ║
║  📊 Frontend logs will appear in the separate window                        ║
║                                                                              ║
║  🏁 Press Ctrl+C to stop all services.                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝

📋 API Server Logs:
""")
        
        # Monitor backend (frontend runs in separate window)
        try:
            self.monitor_backend()
        except KeyboardInterrupt:
            pass
        finally:
            self.shutdown()

def main():
    """Entry point"""
    launcher = F1DashboardDebugLauncher()
    launcher.run()

if __name__ == "__main__":
    main() 