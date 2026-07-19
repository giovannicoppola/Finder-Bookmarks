#!/usr/bin/env python3
"""
Add a bookmark: add_bookmark.py "Title" "/path/to/target".
Prints a message to stdout for the "bookmark created" notification.
"""

import os
import sys
import uuid

import common


def add_bookmark(title, path):
    bookmarks, error = common.load_bookmarks()

    if error:
        # Never overwrite a corrupted database: that would silently destroy
        # every existing bookmark. Leave the file for manual recovery.
        print("Error: bookmarks file is corrupted, nothing saved: {}".format(error), file=sys.stderr)
        print("⚠️ NOT saved — bookmarks file is corrupted")
        sys.exit(1)

    existing = bookmarks.get(title)
    if existing:
        # Same title again: update the path but keep the id and tags
        existing["path"] = path
        message = '"{}" updated to point to: {}'.format(title, path)
    else:
        bookmarks[title] = {"path": path, "id": str(uuid.uuid4()), "tags": []}
        message = '"{}" added, pointing to: {}'.format(title, path)

    common.save_bookmarks(bookmarks)

    print(message, file=sys.stderr)
    print(title)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: python3 add_bookmark.py "Bookmark Title" "Bookmark Path"', file=sys.stderr)
        sys.exit(1)

    title = sys.argv[1].strip()
    path = os.path.expanduser(sys.argv[2])

    if not title:
        print("Error: bookmark title cannot be empty", file=sys.stderr)
        print("⚠️ NOT saved — empty bookmark name")
        sys.exit(1)

    add_bookmark(title, path)
