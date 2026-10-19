"""Library Management System - Simulation Script.

Demonstrates library collection management by registering multiple media items,
simulating checkouts, and querying available titles.
"""

from custom_classes import Book, DVD, LibraryCollection, MediaItem


def main() -> None:
    """Execute the library simulation workflow."""
    my_library = LibraryCollection()

    # Populate collection with diverse media item types (books, movies, and physical games)
    book1 = Book("1984", "George Orwell", 328)
    movie_dvd1 = DVD("Recep Ivedik", "Gokhan Sahan", "156 mins")
    generic_item1 = MediaItem("Monopoly Game", "Hasbro")
    book2 = Book("Nutuk", "Mustafa Kemal Ataturk", 500)
    movie_dvd2 = DVD("The Matrix", "Wachowskis", "136 mins")
    generic_item2 = MediaItem("Chess Set", "Classic Games Inc.")

    for item in [book1, movie_dvd1, generic_item1, book2, movie_dvd2, generic_item2]:
        my_library.add_item(item)
    print("Items added to the library.")

    # Target specific items for batch checkout simulation
    items_to_checkout = [book1, movie_dvd1, book2, movie_dvd2]

    print("\nSimulating checkouts...")
    for item in items_to_checkout:
        status = item.checkout()
        print(f"Checked out '{item.title}' : {status}")

    print("\nAvailable titles remaining:")
    available = my_library.list_available()
    print(available)


if __name__ == "__main__":
    main()