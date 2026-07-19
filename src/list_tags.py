#!/usr/bin/env python3
"""
Script filter: list all tags with bookmark counts.
Selecting a tag sets searchTag and re-opens the bookmark list filtered by it.
"""

import sys

import common


def main():
    search_query = sys.argv[1].strip() if len(sys.argv) > 1 else ""
    if search_query in ("$1", "{var:userInputString}"):
        search_query = ""

    bookmarks, error = common.load_bookmarks()

    if error:
        print(common.alfred_response([
            common.alfred_error_item(
                "Error reading bookmarks", error, icon=common.ALERT_STOP_ICON
            )
        ]))
        return

    if not bookmarks:
        print(common.alfred_response([
            common.alfred_error_item(
                "No bookmarks found", "The database is empty. Add some bookmarks first!"
            )
        ]))
        return

    all_tags = common.get_all_tags(bookmarks)

    if not all_tags:
        print(common.alfred_response([
            common.alfred_error_item(
                "No tags found", "Add some tags to your bookmarks first!"
            )
        ]))
        return

    query_lower = search_query.lower()
    matching_tags = [
        (tag, count) for tag, count in all_tags
        if not query_lower or query_lower in tag.lower()
    ]

    total_count = len(matching_tags)
    items = []

    for idx, (tag, count) in enumerate(matching_tags, 1):
        items.append({
            "title": "{} ({})".format(tag, count),
            "subtitle": "{}/{} Show {} bookmark{} with this tag".format(
                common.format_number(idx),
                common.format_number(total_count),
                common.format_number(count),
                "s" if count != 1 else "",
            ),
            "arg": tag,
            "valid": True,
            "variables": {
                "searchTag": tag,
                "mySource": "tagList",
                # Open the bookmark list unfiltered
                "userInputString": "",
            },
            "icon": {"type": "fileicon", "path": common.GENERIC_FOLDER_ICON},
        })

    if not items:
        items.append(common.alfred_error_item(
            "No tags match your search", "No results for: {}".format(search_query)
        ))

    print(common.alfred_response(items))


if __name__ == "__main__":
    main()
