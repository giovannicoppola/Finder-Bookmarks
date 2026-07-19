#!/usr/bin/env python3
"""
Script filter: list bookmarks, filtered by query and optionally by tag
(searchTag env var, set when arriving from the tag list).
"""

import json
import os
import sys

import common


def list_bookmarks(query="", variables=None):
    """Return the Alfred JSON for the bookmark list."""
    output = {"items": []}
    if variables:
        output["variables"] = variables

    bookmarks, error = common.load_bookmarks()

    if error:
        output["items"].append(
            common.alfred_error_item(
                "Error reading bookmarks",
                "The bookmarks file appears to be corrupted: {}".format(error),
                icon=common.ALERT_STOP_ICON,
            )
        )
        return json.dumps(output)

    if not bookmarks:
        output["items"].append(
            common.alfred_error_item(
                "No bookmarks found",
                "Add bookmarks using the bookmark action or keyword",
            )
        )
        return json.dumps(output)

    tag_filter = os.environ.get("searchTag", "").strip()
    query_lower = str(query).lower().strip() if query else ""

    matching = []
    for title, data in bookmarks.items():
        path = data.get("path", "")
        tags = data.get("tags", [])

        if tag_filter and tag_filter not in tags:
            continue

        if query_lower:
            matches = (
                query_lower in title.lower()
                or query_lower in path.lower()
                or any(query_lower in tag.lower() for tag in tags)
            )
            if not matches:
                continue

        matching.append((title, path, data.get("id", ""), tags))

    total_count = len(matching)

    for idx, (title, path, bookmark_id, tags) in enumerate(matching, 1):
        subtitle_parts = [
            "{}/{}".format(common.format_number(idx), common.format_number(total_count)),
            path,
        ]
        if tags:
            subtitle_parts.append("🏷️ {}".format(", ".join(tags)))

        # Payload for the tag menu (ctrl modifier)
        bookmark_json = json.dumps({"id": bookmark_id, "title": title, "tags": tags})

        mods = {
            "alt+cmd": {
                "subtitle": "⌥⌘: Delete bookmark",
                "arg": bookmark_id,
                "valid": True,
            },
            "alt": {
                "subtitle": "⌥: Rename bookmark",
                "arg": bookmark_id,
                "valid": True,
                "variables": {"bookmarkToRename": bookmark_id},
            },
            "ctrl": {
                "subtitle": "⌃: Add/remove tags",
                "arg": bookmark_json,
                "valid": True,
            },
            # Browse tags (or go back to the tag list); reset session state
            # so the tag list opens fresh.
            "shift": {
                "subtitle": "⇧: Browse tags",
                "arg": "",
                "valid": True,
                "variables": {"userInputString": "", "searchTag": "", "mySource": ""},
            },
        }

        output["items"].append(
            {
                "title": title,
                "subtitle": " • ".join(subtitle_parts),
                "arg": path,
                "valid": True,
                "icon": (
                    {"type": "fileicon", "path": path}
                    if os.path.exists(os.path.expanduser(path))
                    else {"type": "fileicon", "path": common.GENERIC_FOLDER_ICON}
                ),
                "mods": mods,
            }
        )

    if not output["items"] and query_lower:
        output["items"].append(
            common.alfred_error_item(
                "No bookmarks found matching '{}'".format(query),
                "Try a different search term",
            )
        )

    return json.dumps(output)


if __name__ == "__main__":
    # The current user input always arrives as $1 (never via env var, which
    # may be stale when re-entering through an external trigger).
    query = sys.argv[1].strip() if len(sys.argv) > 1 else ""

    # Drop literal variable references that Alfred did not expand
    if query in ("{var:userInputString}", "$1"):
        query = ""

    # Preserve the current query for subsequent workflow steps
    variables = {"userInputString": query}
    for var in ("searchTag", "mySource"):
        value = os.environ.get(var, "").strip()
        if value:
            variables[var] = value

    print(list_bookmarks(query, variables=variables))
