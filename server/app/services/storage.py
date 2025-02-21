import json
import os

# File path for storing data
STORAGE_FILE = "server/app/data/storage.json"

# Ensure the storage file exists
if not os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "w") as f:
        json.dump({}, f)

def load_storage():
    """Load data from JSON file."""
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}  # Return an empty dictionary if file is corrupted

def save_storage(storage):
    """Save data to JSON file."""
    with open(STORAGE_FILE, "w") as f:
        json.dump(storage, f, indent=2)

def save_data(key: str, data: dict):
    """Save data to JSON storage."""
    storage = load_storage()
    storage[key] = data
    save_storage(storage)
    return {"message": "Data saved successfully"}

def get_data(key: str):
    """Retrieve data from JSON storage."""
    storage = load_storage()
    if key in storage:
        return storage[key]
    return {"error": "Data not found"}

def clear_storage():
    """Clear all data in storage."""
    save_storage({})
    return {"message": "Storage cleared successfully"}

def export_storage():
    """Export storage as JSON."""
    return load_storage()