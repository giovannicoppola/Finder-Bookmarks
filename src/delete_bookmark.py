#!/usr/bin/env python3

import os
import json
import sys

def delete_bookmark(title):
    """
    Delete a bookmark from the finder-bookmarks.json file.
    
    Args:
        title (str): The title of the bookmark to delete
        
    Returns:
        bool: True if bookmark was deleted, False if not found or error occurred
    """
    # Expand the tilde to the home directory
    home = os.path.expanduser("~")
    
    # Define the file path
    data_dir = os.path.join(home, "Library/Application Support/Alfred/Workflow Data/giovanni.finder-bookmarks")
    json_file = os.path.join(data_dir, "finder-bookmarks.json")
    
    # Check if file exists
    if not os.path.exists(json_file):
        print(f"Error: Bookmarks file not found at {json_file}", file=sys.stderr)
        return False
    
    # Read the bookmarks file
    try:
        with open(json_file, 'r') as f:
            bookmarks = json.load(f)
    except json.JSONDecodeError:
        print("Error: The bookmarks file appears to be corrupted", file=sys.stderr)
        return False
    
    # Check if the bookmark exists
    if title not in bookmarks:
        print(f"Error: Bookmark '{title}' not found", file=sys.stderr)
        return False
    
    # Store the path before deletion (for output)
    deleted_path = bookmarks[title]
    
    # Delete the bookmark
    del bookmarks[title]
    
    # Write the updated bookmarks back to the file
    try:
        with open(json_file, 'w') as f:
            json.dump(bookmarks, f, indent=2)
    except Exception as e:
        print(f"Error writing to bookmarks file: {e}", file=sys.stderr)
        return False
    
    # Print success message to stderr for logging purposes
    print(f"Bookmark '{title}' pointing to '{deleted_path}' has been deleted", file=sys.stderr)
    
    
    return True

if __name__ == "__main__":
    # Check if we have the right number of arguments
    if len(sys.argv) != 2:
        print("Usage: python delete_bookmark.py \"Bookmark Title\"", file=sys.stderr)
        sys.exit(1)
    
    title = sys.argv[1]
    
    # Delete the bookmark
    success = delete_bookmark(title)
    if success:
        print(f"Bookmark '{title}' deleted successfully")
    else:
        print(f"Failed to delete bookmark '{title}'", file=sys.stderr)
    
    # Exit with appropriate status code
    sys.exit(0 if success else 1)