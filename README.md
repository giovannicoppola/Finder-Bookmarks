# Finder Bookmarks

A bookmark manager for Finder

<a href="https://github.com/giovannicoppola/Finder-Bookmarks/releases/latest/">
<img alt="Downloads"
src="https://img.shields.io/github/downloads/giovannicoppola/Finder-Bookmarks/total?color=purple&label=Downloads"><br/>
</a>

I often find myself typing `pin` to search for a file or folder on my machine. beyond spotlight's scope, or with common names and rarely used, or just I can't seem to remember. 
After considering alternatives (Finder Tags, ForkLift, Path Finder etc.) I concluded that a simple Alfred workflow is the best solution for me, so here it is. 
This is a simple bookmark manager for Finder that allows you to save and quickly access your favorite folders.
Examples: an application support folder, the location of some databases I consult often, like the notes database etc, Alfred workflow preferences etc. or excluded from Spotlight/Alfred scope.

## Features

- Save and access frequently used folders and files 
- Open bookmarks directly in Finder in a terminal or file manager (Terminal, Ghostty, iTerm, WezTerm, Yazi)
- Organize bookmarks with tags and browse by tag, rename, delete
- Copy bookmark paths to clipboard

## Why Finder Bookmarks?

While macOS provides built-in favorites in the Finder sidebar, they can become cluttered and hard to navigate when you have many projects or locations. Finder Bookmarks provides a more flexible and keyboard-centric approach to managing your important locations through Alfred.

## How to Use

### Creating Bookmarks

You can create bookmarks in two ways:

1. **From Alfred File Browser**: Select any file or folder in Alfred's file browser, then use the "Create Finder Bookmark" action from the actions menu. Enter a name for your bookmark when prompted.

2. **From Finder**: Select any file or folder in Finder, then use the File Action workflow to create a bookmark.

### Accessing Bookmarks

Type the workflow keyword (default `bbf`, configurable in the workflow settings), or optional hotkey, followed by an optional search term to filter your bookmarks by name, path, or tag. On any result:

- **Enter**: Open the bookmarked location in Finder (files are revealed in their parent folder)
- **⌘**: Open the file directly
- **⌥**: Rename the bookmark
- **⌃**: Add or remove tags
- **⇧**: Browse bookmarks by tag
- **⌃⌘**: Open in your configured terminal/file manager (Terminal, Ghostty, iTerm, WezTerm, or Yazi)
- **⇧⌘**: Copy the path to the clipboard
- **⌥⌘**: Delete the bookmark

### Tags

Add tags to a bookmark with **⌃** on any result; type to filter existing tags or create a new one. Browse all tags with the tag keyword (default `qqt`, configurable) or with **⇧** from the bookmark list, then select a tag to see the bookmarks carrying it.

## Installation

1. Download the workflow file from the releases section
2. Double-click to install in Alfred
3. Requires Alfred Powerpack

## Technical Details

Bookmarks are stored in a JSON file at:
`~/Library/Application Support/Alfred/Workflow Data/giovanni.finder-bookmarks/finder-bookmarks.json`

## Acknowledgments

- The Alfred community for inspiration and support
- Copilot/Claude Sonnet 🤖 who helped, fixed bugs, and helped write this README 
- DALL-E created the workflow icon 

## Feedback and Contributions

Feedback, bug reports, and feature requests are welcome! Please create an issue on GitHub or reach out directly.

## AI Disclaimer

Like many applications these days, this workflow was built for personal use with help from AI. I'm sharing it here in case others have the same use case and want to save some time and money.

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

- v1.0.0 - Initial release: bookmarks with tags, rename, delete, copy path; open in Finder, Terminal, Ghostty, iTerm, WezTerm or Yazi; notification when a bookmarked path no longer exists
