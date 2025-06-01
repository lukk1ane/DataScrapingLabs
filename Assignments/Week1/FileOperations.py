import json
import os
import shutil
import lorem

def validate_file(file_path):
    """Check if the file exists and is accessible."""
    return os.path.isfile(file_path) and os.access(file_path, os.R_OK)

def read_file(file_path):
    """Read the content of a file with error handling."""
    if not validate_file(file_path):
        print(f"Error: File '{file_path}' does not exist or is not readable.")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def write_file(file_path, data):
    """Write data to a file with error handling."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(data)
        print(f"Data successfully written to {file_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")

def append_to_file(file_path, data):
    """Append data to a file."""
    try:
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(data + '\n')
        print(f"Data successfully appended to {file_path}")
    except Exception as e:
        print(f"Error appending to file: {e}")

def backup_file(file_path):
    """Create a backup of a file."""
    if not validate_file(file_path):
        print(f"Error: Cannot create backup. File '{file_path}' does not exist.")
        return None
    backup_path = f"{file_path}.backup"
    try:
        shutil.copy(file_path, backup_path)
        print(f"Backup created: {backup_path}")
        return backup_path
    except Exception as e:
        print(f"Error creating backup: {e}")
        return None

def parse_csv(file_path):
    """Parse CSV file and return data as a list of dictionaries."""
    if not validate_file(file_path):
        print(f"Error: File '{file_path}' does not exist or is not readable.")
        return None
    try:
        with open(file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            return list(reader)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None

def process_json(file_path):
    """Load and process JSON data from a file."""
    if not validate_file(file_path):
        print(f"Error: File '{file_path}' does not exist or is not readable.")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

def clean_text(text):
    """Perform basic string manipulation: trimming, lowercasing, and removing extra spaces."""
    return ' '.join(text.strip().lower().split())

def filter_data(data, key, value):
    """Filter a list of dictionaries by a specific key-value pair."""
    if not isinstance(data, list):
        print("Error: Data must be a list of dictionaries.")
        return None
    return [item for item in data if item.get(key) == value]


if __name__ == "__main__":
    data_file = "data.txt"
    write_file(data_file, lorem.text())
    append_to_file(data_file, "\nAdding a new line.")
    content = read_file(data_file)
    if content:
        print("File Content:")
        print(content)
    backup_file(data_file)

    csv_data = parse_csv("data.csv")
    if csv_data:
        print("CSV Data:", csv_data)

    json_data = process_json("data.json")
    if json_data:
        print("JSON Data:", json_data)

    cleaned_text = clean_text("   Hello, WORLD!   ")
    print("Cleaned Text:", cleaned_text)

    filtered_data = filter_data(csv_data, "name", "John")
    if filtered_data:
        print("Filtered Data:", filtered_data)

