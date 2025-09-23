# src/utils/helpers.py
import os
import pandas as pd
import json

def create_path(*path_segments):
    return os.path.join(*(str(segment) for segment in path_segments))

def create_dir(*path_segments):
    file_path = create_path(*path_segments)
    os.makedirs(file_path, exist_ok=True)
    return file_path

def save_csv(df, *path_segments):
    file_path = create_path(*path_segments)
    df.to_csv(file_path, index=False)
    print(f"Saved {file_path}")

def load_csv(*path_segments):
    file_path = create_path(*path_segments)
    if os.path.exists(file_path):
        print(f"Loaded {file_path}")
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
def save_json(data, *path_segments):
    file_path = create_path(*path_segments)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved {file_path}")

def load_json(*path_segments):
    file_path = create_path(*path_segments)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        print(f"Loaded {file_path}")
        return data
    else:
        raise FileNotFoundError(f"The file at {file_path} does not exist.")
    
def missing_file(raw_dir, ticker, file_name):
    if not os.path.exists(raw_dir, file_name):
        print(f"Skipping {ticker}: {file_name} not found")
        return True
    return False
