# Scripts Directory

This directory contains utility scripts and launchers for the F1 Analytics Dashboard.

## Launcher Scripts

- **`start_dashboard.py`** - Full dashboard launcher (backend + frontend)
- **`start_backend_only.py`** - Backend API server only 
- **`start_dashboard_debug.py`** - Debug mode with verbose logging
- **`start_frontend.py`** - Frontend development server only
- **`start_backend.py`** - Simple backend launcher

## Test Scripts

- **`test_api_endpoints.py`** - API endpoint testing
- **`test_fixes.py`** - System validation tests

## Usage

From the project root directory:

```bash
# Full dashboard
python scripts/start_dashboard.py

# Backend only
python scripts/start_backend_only.py

# Debug mode
python scripts/start_dashboard_debug.py
```

Or use the simple launcher in the root directory:

```bash
python start_dashboard.py
``` 