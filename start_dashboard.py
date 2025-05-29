#!/usr/bin/env python3
"""
F1 Analytics Dashboard Launcher
Simple wrapper to start the main dashboard
"""

import os
import sys
import subprocess

def main():
    """Launch the F1 Analytics Dashboard"""
    print("🏎️  Starting F1 Analytics Dashboard...")
    
    # Path to the main launcher script
    main_script = os.path.join("scripts", "start_dashboard.py")
    
    if not os.path.exists(main_script):
        print("❌ Main launcher script not found!")
        print(f"   Expected: {main_script}")
        return 1
    
    try:
        # Execute the main launcher
        result = subprocess.run([sys.executable, main_script], 
                              capture_output=False, 
                              text=True)
        return result.returncode
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 