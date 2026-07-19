#!/usr/bin/env python3
"""
Script filter: show tags to add to / remove from one bookmark.
$1 = bookmark JSON ({"id", "title", "tags"}) from the ctrl modifier,
$2 = optional filter text typed by the user.
"""

import json
import sys
import os

import common


def main():
    bookmark_json = sys.argv[1].strip() if len(sys.argv) >= 2 else ""

    # Literal variable reference that Alfred did not expand
    if bookmark_json == "$myInput":
        bookmark_json = os.environ.get("myInput", "").strip()

    if not bookmark_json:
        print(common.alfred_response([
            common.alfred_error_item("Error: no bookmark data provided", "Please try again")
        ]))
        sys.exit(1)

    try:
        bookmark_data = json.loads(bookmark_json)
        bookmark_id = bookmark_data.get("id", "")
        title = bookmark_data.get("title", "Untitled")
        current_tags = bookmark_data.get("tags", [])
    except json.JSONDecodeError as e:
        print(common.alfred_response([
            common.alfred_error_item(
                "Error: invalid bookmark data", "Could not parse JSON: {}".format(e)
            )
        ]))
        sys.exit(1)

    filter_query = sys.argv[2].strip() if len(sys.argv) > 2 else ""
    if filter_query in ("$1", "{var:userInputString}"):
        filter_query = ""
    filter_query = filter_query.lower()

    bookmarks, _ = common.load_bookmarks()
    all_tags = common.get_all_tags(bookmarks)

    items = []

    if not filter_query:
        items.append({
            "title": "Manage tags for: {}".format(title),
            "subtitle": "Currently: {} • Type to filter or create a new tag".format(
                ", ".join(current_tags) if current_tags else "No tags"
            ),
            "valid": False,
        })

    matching_tags = [
        (tag, count) for tag, count in all_tags
        if not filter_query or filter_query in tag.lower()
    ]
    total_count = len(matching_tags)

    def tag_item(tag, subtitle, action):
        return {
            "title": tag,
            "subtitle": subtitle,
            "arg": json.dumps({
                "id": bookmark_id,
                "title": title,
                "tag": tag,
                "action": action,
            }),
            "valid": True,
            "icon": {"type": "fileicon", "path": common.GENERIC_FOLDER_ICON},
        }

    for idx, (tag, count) in enumerate(matching_tags, 1):
        counter = "{}/{}".format(common.format_number(idx), common.format_number(total_count))
        if tag in current_tags:
            items.append(tag_item(
                tag,
                "{} ❌️ Remove this tag ({} bookmarks)".format(counter, common.format_number(count)),
                "remove",
            ))
        else:
            items.append(tag_item(
                tag,
                "{} 🏷️️ Add this tag ({} bookmarks)".format(counter, common.format_number(count)),
                "add",
            ))

    # Offer to create the typed tag when it doesn't exist yet
    if filter_query and filter_query not in (tag.lower() for tag, _ in all_tags):
        create_idx = common.format_number(total_count + 1)
        item = tag_item(filter_query, "", "add")
        item["title"] = "Create new tag: {}".format(filter_query)
        item["subtitle"] = "{}/{} ➕ Press Enter to create and add this tag".format(
            create_idx, create_idx
        )
        items.append(item)

    if not items:
        items.append({
            "title": "No tags found",
            "subtitle": "Type a new tag name to create it",
            "valid": False,
        })

    print(common.alfred_response(items))


if __name__ == "__main__":
    main()
