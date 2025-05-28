#!/usr/bin/env python3
"""
Frontend Startup Script for F1 Analytics Dashboard
Ensures proper setup before starting React development server
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def setup_frontend():
    """Ensure frontend is properly set up"""
    frontend_path = Path("frontend")
    
    if not frontend_path.exists():
        print("❌ Frontend directory not found!")
        return False
    
    # Ensure public directory exists
    public_path = frontend_path / "public"
    if not public_path.exists():
        print("📁 Creating public directory...")
        public_path.mkdir(exist_ok=True)
        
        # Create required public files if they don't exist
        create_public_files(public_path)
    
    # Ensure node_modules exists
    node_modules = frontend_path / "node_modules"
    if not node_modules.exists():
        print("📦 Installing frontend dependencies...")
        subprocess.run(["npm", "install"], cwd=frontend_path, shell=platform.system() == 'Windows')
    
    return True

def create_public_files(public_path):
    """Create essential public files if missing"""
    
    # Copy files from root public if they exist
    root_public = Path("public")
    if root_public.exists():
        for file in ["favicon.ico", "logo192.png", "logo512.png", "manifest.json", "robots.txt"]:
            src = root_public / file
            dst = public_path / file
            if src.exists() and not dst.exists():
                import shutil
                shutil.copy2(src, dst)
                print(f"✅ Copied {file} to frontend/public/")

def start_frontend():
    """Start the React development server"""
    frontend_path = Path("frontend")
    
    print("🎨 Starting F1 Dashboard frontend...")
    print("🔗 Frontend URL: http://localhost:3000")
    print("🏁 Press Ctrl+C to stop the server")
    print("="*60)
    
    try:
        if platform.system() == 'Windows':
            subprocess.run(["cmd", "/c", "npm", "start"], cwd=frontend_path)
        else:
            subprocess.run(["npm", "start"], cwd=frontend_path)
    except KeyboardInterrupt:
        print("\n🛑 Frontend server stopped.")

def main():
    """Main execution"""
    if setup_frontend():
        start_frontend()
    else:
        print("❌ Failed to set up frontend.")
        sys.exit(1)

if __name__ == "__main__":
    main() 