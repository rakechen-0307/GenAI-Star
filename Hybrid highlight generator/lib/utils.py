import os

def get_all_files(folder_path):
    # List all entries in the directory
    entries = os.listdir(folder_path)
    
    # Filter out only files
    files = [entry for entry in entries if os.path.isfile(os.path.join(folder_path, entry))]
    
    return files

