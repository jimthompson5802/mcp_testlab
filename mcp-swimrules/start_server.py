#!/usr/bin/env python3
"""
Startup script for Swim Rules Agent Web Application
"""
import sys
import subprocess
from pathlib import Path


def main():
    """Main startup function"""
    print("🏊 Starting Swim Rules Agent Web Application...")

    # Check if we're in the right directory
    if not Path("app_server.py").exists():
        print("❌ Error: app_server.py not found. Please run this script from the mcp-swimrules directory.")
        sys.exit(1)

    # Check if templates and static directories exist
    if not Path("templates").exists() or not Path("static").exists():
        print("❌ Error: templates or static directory not found.")
        sys.exit(1)

    try:
        # Start the FastAPI server
        print("🚀 Starting FastAPI server on http://localhost:8000")
        print("📝 Open your browser and navigate to http://localhost:8000")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)

        subprocess.run(
            [sys.executable, "-m", "uvicorn", "app_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
        )

    except KeyboardInterrupt:
        print("\n👋 Shutting down Swim Rules Agent Web Application...")
    except FileNotFoundError:
        print("❌ Error: uvicorn not found. Please install dependencies with:")
        print("   pip install -r requirements_web.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
