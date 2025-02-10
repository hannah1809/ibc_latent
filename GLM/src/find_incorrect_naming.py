import os
import re

def search_files(directory, keyword):
    if not os.path.exists(directory):
        print(f"Directory does not exist: {directory}")
        return []

    matching_files = []
    for root, _, files in os.walk(directory):
        print(f"Searching in directory: {root}")  # Debugging statement
        if not files:
            print(f"No files found in directory: {root}")  # Debugging statement
        for file in files:
            if keyword in file and file.endswith('.nii.gz'):
                print(f"Found matching file: {file}")  # Debugging statement
                matching_files.append(os.path.join(root, file))
    
    matching_files.sort()  # Sort the list alphabetically
    return matching_files

def extract_tasks(files):
    task_pattern = re.compile(r'task-(.*?)_dir')
    tasks = set()
    for file in files:
        match = task_pattern.search(file)
        if match:
            tasks.add(match.group(1))
    return tasks

directory = '/home/hmueller2/Downloads/ibc_all'
keyword = 'run'
matching_files = search_files(directory, keyword)

print(f"Total matching files: {len(matching_files)}")  # Debugging statement
for file in matching_files:
    print(file)

tasks = extract_tasks(matching_files)
print(f"Unique tasks: {tasks}")