import os
from pathlib import Path

def obtain_paths_docs(folder):
    """
    Return list with all the paths of the files in a specific folder
    Use for looping
    """
    path_docs = []
    for folder_path, _, files in os.walk(folder):
        for file in files:
            complete_path = os.path.join(folder_path, file)
            path_docs.append(complete_path)
    return path_docs

if __name__ == "__main__":
    print(obtain_paths_docs("BL"))