#!/usr/bin/env python3
"""
Shared helpers for the Finder Bookmarks workflow.

Bookmark database format:
    {"title": {"path": "/some/path", "id": "uuid", "tags": ["tag1", ...]}}
Legacy format ({"title": "/some/path"}) is migrated on load.
"""

import json
import os
import sys
import uuid
from typing import NoReturn

BUNDLE_ID = "giovanni.finder-bookmarks"

GENERIC_FOLDER_ICON = (
    "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/GenericFolderIcon.icns"
)
ALERT_NOTE_ICON = (
    "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertNoteIcon.icns"
)
ALERT_STOP_ICON = (
    "/System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/AlertStopIcon.icns"
)


def get_data_dir():
    """Workflow data directory: Alfred provides it via env var; fall back to
    the conventional location so the scripts also work from a terminal."""
    data_dir = os.environ.get("alfred_workflow_data")
    if not data_dir:
        data_dir = os.path.join(
            os.path.expanduser("~"),
            "Library/Application Support/Alfred/Workflow Data",
            BUNDLE_ID,
        )
    os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_bookmarks_file():
    return os.path.join(get_data_dir(), "finder-bookmarks.json")


def migrate_bookmarks(bookmarks):
    """Bring a bookmarks dict to the current format (path/id/tags per entry)."""
    migrated = {}
    for title, value in bookmarks.items():
        if isinstance(value, str):
            migrated[title] = {"path": value, "id": str(uuid.uuid4()), "tags": []}
        elif isinstance(value, dict):
            if "id" not in value:
                value["id"] = str(uuid.uuid4())
            if "tags" not in value:
                value["tags"] = []
            migrated[title] = value
    return migrated


def load_bookmarks():
    """
    Read the bookmarks database.

    Returns (bookmarks, error): on success error is None; if the file is
    corrupted, bookmarks is {} and error describes the problem. The corrupted
    file is left untouched on disk so it can be recovered by hand.
    A legacy-format file is migrated and persisted once.
    """
    json_file = get_bookmarks_file()
    if not os.path.exists(json_file):
        return {}, None

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            raw = json.load(f)
        if not isinstance(raw, dict):
            raise ValueError("bookmarks file does not contain a JSON object")
    except (json.JSONDecodeError, ValueError) as e:
        return {}, "{} ({})".format(json_file, e)

    bookmarks = migrate_bookmarks(raw)
    if bookmarks != raw:
        save_bookmarks(bookmarks)
    return bookmarks, None


def save_bookmarks(bookmarks):
    """Write the database atomically (temp file + rename), so a crash or two
    concurrent script runs can never leave a half-written file behind."""
    json_file = get_bookmarks_file()
    tmp_file = "{}.{}.tmp".format(json_file, os.getpid())
    try:
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(bookmarks, f, indent=2, ensure_ascii=False)
        os.replace(tmp_file, json_file)
    finally:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)


def find_title_by_id(bookmarks, bookmark_id):
    """Return the title of the bookmark with this id, or None."""
    for title, data in bookmarks.items():
        if isinstance(data, dict) and data.get("id") == bookmark_id:
            return title
    return None


def is_uuid(text):
    try:
        uuid.UUID(text)
        return True
    except (ValueError, AttributeError, TypeError):
        return False


def get_all_tags(bookmarks):
    """All unique tags with usage counts, sorted by count desc then name."""
    tag_counts = {}
    for data in bookmarks.values():
        for tag in data.get("tags", []) if isinstance(data, dict) else []:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    return sorted(tag_counts.items(), key=lambda x: (-x[1], x[0].lower()))


def format_number(num):
    """Format a number with thousand separators."""
    if num is None:
        return "0"
    try:
        return "{:,}".format(int(num))
    except (ValueError, TypeError):
        return str(num)


def alfred_response(items, variables=None):
    """JSON string for a script filter: items plus optional session variables."""
    response = {"items": items}
    if variables:
        response["variables"] = variables
    return json.dumps(response, ensure_ascii=False)


def alfred_error_item(title, subtitle, icon=ALERT_NOTE_ICON):
    return {
        "title": title,
        "subtitle": subtitle,
        "arg": "",
        "valid": False,
        "icon": {"type": "fileicon", "path": icon},
    }


def notification(title, subtitle=""):
    """JSON string that downstream notification nodes read via
    {var:notification_title} / {var:notification_subtitle}."""
    return json.dumps(
        {
            "alfredworkflow": {
                "variables": {
                    "notification_title": title,
                    "notification_subtitle": subtitle,
                }
            }
        }
    )


def notify_and_exit(title, subtitle="", code=1) -> NoReturn:
    print(notification(title, subtitle))
    sys.exit(code)
