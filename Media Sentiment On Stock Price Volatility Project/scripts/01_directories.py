# scripts/01_directories.py
from src.utils.helpers import create_dir, save_json
from config import settings

def project_directories(tickers):
    """ creates all required directories for the scripts and returns a dictionary of paths"""

    dirs = {
        "base": create_dir("data"),
        "raw": create_dir("data", "raw"),
        "processed": create_dir("data", "processed"),
        "tickers":{}
    }
    
    for ticker in tickers:
        dirs["tickers"][ticker] = {
            "raw": create_dir("data", "raw", ticker), 
            "processed": create_dir("data", "processed", ticker)}

    return dirs

def main():
    print("Setting up project directories...")

    # create project directories, saving structure into project_paths.json
    dirs = project_directories(settings.TICKERS)
    save_json(dirs, "project_paths.json")
    
    print("Setup Complete!")

if __name__ == "__main__":
    main()