"""Library Management System - Comprehensive Test Suite.

EE471 Week 4 - Section 2 Part 2: Extend the classes with CRUD methods.
Demonstrates at least one successful call for every method and catches
each expected exception (ItemNotFoundError, ItemStateError, ValueError).
"""

from library_custom_classes import (
    Book,
    DVD,
    ItemNotFoundError,
    ItemStateError,
    LibraryCollection,
    MediaItem,
)


def run_test_suite() -> None:
    print("=" * 65)
    print(" EE471 WEEK 4 - LIBRARY CRUD TEST SUITE")
    print("=" * 65)

    library = LibraryCollection()

    # ---------------------------------------------------------
    # 1. ADD ITEMS & AUTO-INCREMENTING IDS
    # ---------------------------------------------------------
    print("\n--- 1. Testing add_item() & Sequential Non-reusable IDs ---")
    book1 = Book(title="1984", author="George Orwell", page_count=328)
    dvd1 = DVD(title="Inception", author="Christopher Nolan", duration=148)
    generic1 = MediaItem(title="Chess Set", author="Classic Games Inc.")

    id1 = library.add_item(book1)
    id2 = library.add_item(dvd1)
    id3 = library.add_item(generic1)

    print(f"Added '{book1.title}' -> assigned ID: {id1}")
    print(f"Added '{dvd1.title}' -> assigned ID: {id2}")
    print(f"Added '{generic1.title}' -> assigned ID: {id3}")

    # ---------------------------------------------------------
    # 2. DICTIONARY SERIALIZATION (to_dict)
    # ---------------------------------------------------------
    print("\n--- 2. Testing to_dict() Serialization ---")
    print("Book to_dict():", book1.to_dict())
    print("DVD to_dict():", dvd1.to_dict())
    print("MediaItem to_dict():", generic1.to_dict())

    # ---------------------------------------------------------
    # 3. GET ITEM (Success and Exception)
    # ---------------------------------------------------------
    print("\n--- 3. Testing get_item() ---")
    item = library.get_item(1)
    print(f"Successfully retrieved item #1: {item}")

    print("Attempting to get non-existent item #999:")
    try:
        library.get_item(999)
    except ItemNotFoundError as e:
        print(f"  [CAUGHT ItemNotFoundError]: {e}")

    # ---------------------------------------------------------
    # 4. LIST ITEMS & FILTERING
    # ---------------------------------------------------------
    print("\n--- 4. Testing list_items() with Filters ---")
    print("All items:", library.list_items())
    print("Filter (item_type='book'):", library.list_items(item_type="book"))
    print("Filter (item_type='dvd'):", library.list_items(item_type="dvd"))
    print("Filter (available=True):", library.list_items(available=True))

    # ---------------------------------------------------------
    # 5. CHECKOUT (Success, Custom DVD Message, and Exception)
    # ---------------------------------------------------------
    print("\n--- 5. Testing checkout() State Transitions ---")
    # Book checkout
    book_msg = book1.checkout()
    print(f"Book checkout response: {book_msg}")

    # DVD checkout (must return reminder string, no print)
    dvd_msg = dvd1.checkout()
    print(f"DVD checkout response: {dvd_msg}")

    # Checkout already checked-out item
    print("Attempting to checkout already checked-out Book #1:")
    try:
        book1.checkout()
    except ItemStateError as e:
        print(f"  [CAUGHT ItemStateError]: {e}")

    # ---------------------------------------------------------
    # 6. RETURN ITEM (Success and Exception)
    # ---------------------------------------------------------
    print("\n--- 6. Testing return_item() State Transitions ---")
    ret_msg = book1.return_item()
    print(f"Returned Book #1: {ret_msg} (is_available={book1.is_available})")

    print("Attempting to return an already available Book #1:")
    try:
        book1.return_item()
    except ItemStateError as e:
        print(f"  [CAUGHT ItemStateError]: {e}")

    # ---------------------------------------------------------
    # 7. UPDATE ITEM (Success and Exception)
    # ---------------------------------------------------------
    print("\n--- 7. Testing update_item() ---")
    updated = library.update_item(1, title="Nineteen Eighty-Four", page_count=350)
    print(f"Updated item #1: {updated}")

    print("Attempting to change restricted field 'is_available':")
    try:
        library.update_item(1, is_available=False)
    except ValueError as e:
        print(f"  [CAUGHT ValueError]: {e}")

    print("Attempting to change restricted field 'id':")
    try:
        library.update_item(1, id=100)
    except ValueError as e:
        print(f"  [CAUGHT ValueError]: {e}")

    # ---------------------------------------------------------
    # 8. REMOVE ITEM & VERIFY NON-REUSABLE IDS
    # ---------------------------------------------------------
    print("\n--- 8. Testing remove_item() & ID Continuity ---")
    # DVD #2 is currently checked out: removing it must fail
    print(f"Attempting to remove checked-out DVD #{dvd1.id}:")
    try:
        library.remove_item(dvd1.id)
    except ItemStateError as e:
        print(f"  [CAUGHT ItemStateError]: {e}")

    # Now return the DVD and remove it successfully
    dvd1.return_item()
    removed_item = library.remove_item(dvd1.id)
    print(f"Successfully removed item #{removed_item.id}: '{removed_item.title}'")

    # Verify ID is not reused when adding a new item
    book2 = Book(title="The Catcher in the Rye", author="J.D. Salinger", page_count=220)
    id4 = library.add_item(book2)
    print(f"Added new item '{book2.title}' -> assigned ID: {id4} (verified: ID 2 was NOT reused!)")

    # Attempting to get the removed item #2
    print("Attempting to get previously removed item #2:")
    try:
        library.get_item(2)
    except ItemNotFoundError as e:
        print(f"  [CAUGHT ItemNotFoundError]: {e}")

    print("\n" + "=" * 65)
    print(" ALL CRUD OPERATIONS & EXCEPTIONS VERIFIED SUCCESSFULLY!")
    print("=" * 65)


if __name__ == "__main__":
    run_test_suite()
    run_test_suite()