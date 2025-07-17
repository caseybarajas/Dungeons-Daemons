#!/usr/bin/env python3
"""
Dungeons & Daemons Launcher
Simple launcher script to run the game from the project root.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main game
if __name__ == "__main__":
    try:
        from src.main import main
        main()
    except ImportError as e:
        print(f"Error importing game modules: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"Unexpected error: {e}")
        input("Press Enter to exit...") 