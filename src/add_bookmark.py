#!/usr/bin/env python3

import os
import json
import sys
from pathlib import Path

def add_bookmark(title, path):
    """
    Add a bookmark to the finder-bookmarks.json file.
    
    Args:
        title (str): The title of the bookmark
        path (str): The path of the bookmark
    """
    # Expand the tilde to the home directory
    home = os.path.expanduser("~")
    
    # Define the directory and file paths
    data_dir = os.path.join(home, "Library/Application Support/Alfred/Workflow Data/giovanni.finder-bookmarks")
    json_file = os.path.join(data_dir, "finder-bookmarks.json")
    
    # Create the directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Initialize the bookmarks dictionary
    bookmarks = {}
    
    # Read the existing file if it exists
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r') as f:
                bookmarks = json.load(f)
        except json.JSONDecodeError:
            # If the file exists but is not valid JSON, start with an empty dictionary
            bookmarks = {}
    
    # Extract just the file name from the path
    file_name = os.path.basename(path)
    
    # Add the new bookmark
    bookmarks[title] = path
    
    # Write the updated bookmarks back to the file
    with open(json_file, 'w') as f:
        json.dump(bookmarks, f, indent=2)
    
    # Print output to stderr for logging
    print(f'Bookmark "{title}" added successfully pointing to: {path}', file=sys.stderr)
    print(f'File name: {file_name}', file=sys.stderr)
    
    # Return the title to stdout for Alfred
    print(title)

if __name__ == "__main__":
    # Check if we have the right number of arguments
    if len(sys.argv) != 3:
        print("Usage: python add_bookmark.py \"Bookmark Title\" \"Bookmark Path\"", file=sys.stderr)
        sys.exit(1)
    
    title = sys.argv[1]
    path = sys.argv[2]
    
    # Expand tilde to home directory in the path if needed
    if path.startswith('~'):
        path = os.path.expanduser(path)
    
    add_bookmark(title, path)