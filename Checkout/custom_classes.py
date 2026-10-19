"""Library Management System - Custom Classes Module.

Defines classes representing various media items (books, DVDs, generic items)
and a collection manager to track availability within a library.
"""


class MediaItem:
    """Represents a generic item in a library collection."""

    def __init__(self, title: str, author: str, is_available: bool = True):
        """Initialize a media item with metadata and availability status."""
        self.title = title
        self.author = author
        self.is_available = is_available

    def checkout(self) -> str:
        """Mark the item as checked out if it is currently available."""
        if self.is_available:
            self.is_available = False
            return "Successful checkout"
        return "Already out"

    def return_item(self) -> None:
        """Mark the item as available in the library collection."""
        self.is_available = True

    def __str__(self) -> str:
        """Return a formatted string displaying title, author, and status."""
        status = "Available" if self.is_available else "Checked Out"
        return f"{self.title} by {self.author} [{status}]"


class Book(MediaItem):
    """Represents a book in the library collection with page count tracking."""

    def __init__(self, title: str, author: str, page_count: int, is_available: bool = True):
        """Initialize a book instance including its specific page count."""
        super().__init__(title, author, is_available)
        self.page_count = page_count

    def __str__(self) -> str:
        """Return a formatted representation containing the book page count."""
        status = "Available" if self.is_available else "Checked Out"
        return f"{self.title} by {self.author} ({self.page_count} pages) [{status}]"


class DVD(MediaItem):
    """Represents a DVD disc with runtime duration and handling instructions."""

    def __init__(self, title: str, author: str, duration: str, is_available: bool = True):
        """Initialize a DVD instance including its runtime duration."""
        super().__init__(title, author, is_available)
        self.duration = duration

    def checkout(self) -> str:
        """Check out the DVD while issuing physical media handling reminders."""
        # Delegates state change and status messaging to the parent class
        # to ensure unified checkout behavior across all media types.
        result = super().checkout()

        # Physical discs require care instructions only when the checkout actually succeeds.
        if result == "Successful checkout":
            print("Handle with care: Do not scratch the disc.")

        return result


class LibraryCollection:
    """Manages an inventory of MediaItem instances and their circulation status."""

    def __init__(self):
        """Initialize an empty library collection."""
        self.items = []

    def add_item(self, item: MediaItem) -> None:
        """Add a MediaItem or any of its subclasses to the collection inventory."""
        self.items.append(item)

    def list_available(self) -> list:
        """Return a list of titles for all items currently available for checkout."""
        return [item.title for item in self.items if item.is_available]