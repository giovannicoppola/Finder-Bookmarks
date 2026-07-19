#!/usr/bin/env python3
"""
Delete a bookmark: delete_bookmark.py "identifier"
The identifier is resolved as a UUID first (what the workflow passes),
then as an exact title, then as a path.
"""

import os
import sys

import common


def resolve_titles(bookmarks, identifier):
    """Return the list of bookmark titles the identifier refers to."""
    if common.is_uuid(identifier):
        title = common.find_title_by_id(bookmarks, identifier)
        return [title] if title else []

    if identifier in bookmarks:
        return [identifier]

    # Fall back to path matching (also catches titles that look like paths)
    target = os.path.normpath(os.path.abspath(os.path.expanduser(identifier)))
    matches = []
    for title, data in bookmarks.items():
        path = data.get("path", "")
        if path and os.path.normpath(os.path.abspath(os.path.expanduser(path))) == target:
            matches.append(title)
    return matches


def delete_bookmark(identifier):
    bookmarks, error = common.load_bookmarks()

    if error:
        print("Error: the bookmarks file appears to be corrupted: {}".format(error), file=sys.stderr)
        return False

    titles = resolve_titles(bookmarks, identifier)
    if not titles:
        print("Error: no bookmark found for '{}'".format(identifier), file=sys.stderr)
        return False

    for title in titles:
        path = bookmarks[title].get("path", "")
        del bookmarks[title]
        print("Deleted bookmark '{}' (path: {})".format(title, path), file=sys.stderr)

    common.save_bookmarks(bookmarks)
    return True


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].strip():
        print('Usage: python3 delete_bookmark.py "Bookmark title, ID, or path"', file=sys.stderr)
        sys.exit(1)

    identifier = sys.argv[1].strip()

    if delete_bookmark(identifier):
        print("Bookmark deleted 🗑️")
        sys.exit(0)
    else:
        print("⚠️ Could not delete bookmark")
        sys.exit(1)
