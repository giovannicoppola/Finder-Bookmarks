#!/usr/bin/env python3

import json
import os
import sys


def list_bookmarks(query=""):
    """
    Read bookmarks from the JSON file and generate Alfred JSON output format.
    Filters bookmarks based on an optional query string.

    Args:
        query (str): Optional query string to filter bookmarks

    Returns:
        str: JSON string formatted for Alfred
    """
    # Expand the tilde to the home directory
    home = os.path.expanduser("~")

    # Define the file path
    data_dir = os.path.join(
        home,
        "Library/Application Support/Alfred/Workflow Data/giovanni.finder-bookmarks",
    )
    json_file = os.path.join(data_dir, "finder-bookmarks.json")

    # Initialize the output structure
    output = {"items": []}

    # Check if the file exists
    if not os.path.exists(json_file):
        # Return a message indicating no bookmarks found
        output["items"].append(
            {
                "title": "No bookmarks found",
                "subtitle": "Add bookmarks using the bookmark action or keyword",
                "arg": "",
                "valid": False,
                "icon": {
                    "type": "fileicon",
                    "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertNoteIcon.icns",
                },
            }
        )
        return json.dumps(output)

    # Read the bookmarks file
    try:
        with open(json_file, "r") as f:
            bookmarks = json.load(f)
    except json.JSONDecodeError:
        # Return a message indicating invalid JSON
        output["items"].append(
            {
                "title": "Error reading bookmarks",
                "subtitle": "The bookmarks file appears to be corrupted",
                "arg": "",
                "valid": False,
                "icon": {
                    "type": "fileicon",
                    "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns",
                },
            }
        )
        return json.dumps(output)

    # If no bookmarks found
    if not bookmarks:
        output["items"].append(
            {
                "title": "No bookmarks found",
                "subtitle": "Add bookmarks using the bookmark action or keyword",
                "arg": "",
                "valid": False,
                "icon": {
                    "type": "fileicon",
                    "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertNoteIcon.icns",
                },
            }
        )
        return json.dumps(output)

    # Filter and add bookmarks to output
    for title, path in bookmarks.items():
        # If query is provided, filter bookmarks
        if (
            query
            and query.lower() not in title.lower()
            and query.lower() not in path.lower()
        ):
            continue

        # Add bookmark to items
        output["items"].append(
            {
                "title": title,
                "subtitle": path,
                "arg": path,
                "valid": True,
                "icon": (
                    {"type": "fileicon", "path": path}
                    if os.path.exists(os.path.expanduser(path))
                    else {
                        "type": "fileicon",
                        "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/GenericFolderIcon.icns",
                    }
                ),
                "mods": {
                    "alt+cmd": {
                        "subtitle": "⌥⌘: Delete bookmark",
                        "arg": title,
                        "valid": True,
                    }
                },
            }
        )

    # If no results after filtering
    if not output["items"]:
        output["items"].append(
            {
                "title": f"No bookmarks found matching '{query}'",
                "subtitle": "Try a different search term",
                "arg": "",
                "valid": False,
                "icon": {
                    "type": "fileicon",
                    "path": "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertNoteIcon.icns",
                },
            }
        )

    return json.dumps(output)


if __name__ == "__main__":
    # Get optional query string from command line arguments
    query = sys.argv[1] if len(sys.argv) > 1 else ""

    # Print Alfred JSON output to stdout
    print(list_bookmarks(query))

