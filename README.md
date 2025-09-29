# Finder Bookmarks

A bookmark manager for Finder

I often find myself typing `pin` to search for a file or folder on my machine. beyond spotlight's scope, or with common names and rarely used, or just I can't seem to remember. 
After considering alternatives (Finder Tags, ForkLift, Path Finder etc.) I concluded that a simple Alfred workflow is the best solution for me, so here it is. 
This is a simple bookmark manager for Finder that allows you to save and quickly access your favorite folders.
Examples: an application support folder, the location of some databases I consult often, like the notes database etc, Alfred workflow preferences etc. or excluded from Spotlight/Alfred scope.

## Features

- Save frequently used folders and files as bookmarks
- Access your bookmarks quickly with a simple keyword
- Open bookmarks directly in Finder
- Option to open bookmark locations in iTerm
- Copy bookmark paths to clipboard
- Delete bookmarks when no longer needed
- File icons shown for easy visual recognition

## Why Finder Bookmarks?

While macOS provides built-in favorites in the Finder sidebar, they can become cluttered and hard to navigate when you have many projects or locations. Finder Bookmarks provides a more flexible and keyboard-centric approach to managing your important locations through Alfred.

## How to Use

### Creating Bookmarks

You can create bookmarks in two ways:

1. **From Alfred File Browser**: Select any file or folder in Alfred's file browser, then use the "Create Finder Bookmark" action from the actions menu. Enter a name for your bookmark when prompted.

2. **From Finder**: Select any file or folder in Finder, then use the File Action workflow to create a bookmark.

### Accessing Bookmarks

Type `g` in Alfred followed by an optional search term to filter your bookmarks. Press Enter on any result to:

- **Enter**: Open the bookmarked location in Finder
- **⌘+⌥**: Delete the bookmark
- **Ctrl**: Open in iTerm
- **⌥**: Copy path to clipboard
- **fn**: Open file directly (if bookmark points to a file) or open folder 

## Installation

1. Download the workflow file from the releases section
2. Double-click to install in Alfred
3. Requires Alfred Powerpack

## Technical Details

Bookmarks are stored in a JSON file at:
`~/Library/Application Support/Alfred/Workflow Data/giovanni.finder-bookmarks/finder-bookmarks.json`

## Acknowledgments

- [Alfred App](https://www.alfredapp.com/) for providing the amazing automation platform
- The Alfred community for inspiration and support
- Copilot/Claude Sonnet 🤖 who helped, fixed bugs, and wrote this README 
- ChatGPT created the workflow icon 

## Feedback and Contributions

Feedback, bug reports, and feature requests are welcome! Please create an issue on GitHub or reach out directly.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## FAQ

**Q: Can I sync my bookmarks across multiple machines?**
A: Yes, if you use Alfred's sync feature, your bookmarks will sync along with other workflow data.

**Q: What happens if I bookmark a file/folder and later move it?**
A: The bookmark stores the absolute path, so if you move the target file/folder, you'll need to update the bookmark.

**Q: Is there a limit to how many bookmarks I can create?**
A: There's no practical limit to the number of bookmarks you can create.

## Version History

- v1.0.0 - Initial release
- [Add future versions as your workflow evolves]
