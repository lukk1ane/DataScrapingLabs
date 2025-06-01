import logging
import os


def list_files(directory):
    """List all files in a given directory."""
    try:
        return os.listdir(directory)
    except Exception as e:
        print(f"Error listing files: {e}")
        return []

def sort_files(directory, by='name'):
    """Sort files in a directory by name, type, or date."""
    try:
        files = os.listdir(directory)
        if by == 'name':
            return sorted(files)
        elif by == 'type':
            return sorted(files, key=lambda x: os.path.splitext(x)[1])
        elif by == 'date':
            return sorted(files, key=lambda x: os.path.getmtime(os.path.join(directory, x)))
        else:
            print("Invalid sort type. Use 'name', 'type', or 'date'.")
            return []
    except Exception as e:
        print(f"Error sorting files: {e}")
        return []

def search_file(directory, filename):
    """Search for a file in a directory."""
    try:
        for root, _, files in os.walk(directory):
            if filename in files:
                return os.path.join(root, filename)
        print("File not found.")
        return None
    except Exception as e:
        print(f"Error searching for file: {e}")
        return None

def setup_logging():
    """Setup logging for file operations."""
    logging.basicConfig(filename='file_operations.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

def log_operation(operation, details):
    """Log file operations."""
    logging.info(f"{operation}: {details}")


if __name__ == '__main__':
    print("Files in directory:", list_files("."))
    print("Sorted files by name:", sort_files(".", "name"))
    print("Searching for sample.txt:", search_file(".", "data.txt"))

    setup_logging()
    log_operation("File Read", "Read data.txt")
