# Path: run.py
from src import main

if __name__ == "__main__":
    main()
    # Load and show settings file location
    import os
    if os.path.exists("settings.json"):
        print("Settings loaded from settings.json")