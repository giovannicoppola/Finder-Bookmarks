#!/usr/bin/env python3
"""
Rename a bookmark. The new name arrives as $1; the bookmark to rename is
identified by the bookmarkToRename variable (UUID or title), set by the
⌥ modifier in the bookmark list.
Prints notification variables for the downstream notification node.
"""

import os
import sys

import common


def main():
    new_name = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    if not new_name:
        common.notify_and_exit("Name cannot be empty", "Please enter a valid bookmark name")

    identifier = os.environ.get("bookmarkToRename", "").strip()
    if not identifier and len(sys.argv) >= 3:
        identifier = sys.argv[2].strip()
    if not identifier:
        common.notify_and_exit(
            "Error: no bookmark identifier found",
            "bookmarkToRename variable or argument is missing",
        )

    bookmarks, error = common.load_bookmarks()
    if error:
        common.notify_and_exit("Error reading bookmarks", error)

    # Resolve by id first (what the workflow passes), then by title
    current_name = common.find_title_by_id(bookmarks, identifier)
    if current_name is None and identifier in bookmarks:
        current_name = identifier

    if current_name is None:
        common.notify_and_exit(
            "Error: bookmark not found", "Could not find bookmark: {}".format(identifier)
        )

    if new_name == current_name:
        common.notify_and_exit("Nothing to rename", "The name is unchanged", code=0)

    if new_name in bookmarks:
        common.notify_and_exit(
            "Error: name already exists",
            "A bookmark named '{}' already exists".format(new_name),
        )

    bookmarks[new_name] = bookmarks.pop(current_name)
    common.save_bookmarks(bookmarks)

    print(common.notification(
        "✓ Bookmark renamed", "{} → {}".format(current_name, new_name)
    ))


if __name__ == "__main__":
    main()
