#!/usr/bin/env python3
"""
Add or remove a tag on a bookmark.
$1 = JSON from tag_menu: {"id", "title", "tag", "action"}.
Prints notification variables for the downstream notification node.
"""

import json
import sys

import common


def main():
    if len(sys.argv) < 2:
        common.notify_and_exit("Error: no action data provided")

    try:
        action_data = json.loads(sys.argv[1])
        bookmark_id = action_data.get("id", "")
        title = action_data.get("title", "Untitled")
        tag = action_data.get("tag", "")
        action = action_data.get("action", "add")
    except json.JSONDecodeError as e:
        common.notify_and_exit("Error: invalid action data", str(e))

    if not bookmark_id or not tag:
        common.notify_and_exit("Error: bookmark ID and tag are required")

    bookmarks, error = common.load_bookmarks()
    if error:
        common.notify_and_exit("Error reading bookmarks", error)

    bookmark_title = common.find_title_by_id(bookmarks, bookmark_id)
    if bookmark_title is None:
        common.notify_and_exit("Error: bookmark not found: {}".format(title))

    tags = bookmarks[bookmark_title]["tags"]

    if action == "add":
        if tag in tags:
            common.notify_and_exit(
                "Tag already exists", "'{}' already on {}".format(tag, title), code=0
            )
        tags.append(tag)
        message = ("✓ Tag added", "Added '{}' to {}".format(tag, title))
    elif action == "remove":
        if tag not in tags:
            common.notify_and_exit("Tag not found", "'{}' not on {}".format(tag, title), code=0)
        tags.remove(tag)
        message = ("✓ Tag removed", "Removed '{}' from {}".format(tag, title))
    else:
        common.notify_and_exit("Error: unknown action '{}'".format(action))

    common.save_bookmarks(bookmarks)
    print(common.notification(*message))


if __name__ == "__main__":
    main()
