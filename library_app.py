"""Library Management System - Flask REST API.

EE471 Week 4 - Section 2 Part 3: Flask REST API
Exposes the LibraryCollection model via RESTful JSON endpoints.
Adheres strictly to the HTTP status code and response schema requirements:
- Error format: {"error": "<message>"}
- Success codes: 200, 201, 204
- Error codes: 400, 404, 409
"""

from typing import Any, Dict
from flask import Flask, jsonify, render_template, request
from library_custom_classes import (
    Book,
    DVD,
    ItemNotFoundError,
    ItemStateError,
    LibraryCollection,
    MediaItem,
)

app = Flask(__name__, template_folder='.', static_folder='.', static_url_path='')

@app.route('/')
def home():
    """Serve the library management frontend."""
    return render_template('library_index.html')


# ---------------------------------------------------------------------------
# Collection Instance & Initial Seeding (At least 3 mixed items)
# ---------------------------------------------------------------------------
library = LibraryCollection()

# Seed items matching assignment specifications & Figma design
library.add_item(Book(title="The Great Gatsby", author="F. Scott Fitzgerald", page_count=180))
library.add_item(DVD(title="Inception", author="Christopher Nolan", duration=148))
library.add_item(Book(title="1984", author="George Orwell", page_count=328))
library.add_item(DVD(title="Arrival", author="Denis Villeneuve", duration=116))


# ---------------------------------------------------------------------------
# Helper function for consistent error responses
# ---------------------------------------------------------------------------
def error_response(message: str, status_code: int):
    """Return JSON error response according to assignment format."""
    return jsonify({"error": message}), status_code


# ---------------------------------------------------------------------------
# REST API Endpoints
# ---------------------------------------------------------------------------

@app.route("/api/items", methods=["POST"])
def create_item():
    """Create a new Book or DVD item.

    Expected JSON body:
        title (str): Title of the item
        author (str): Author / Director name
        type (str): 'book' or 'dvd'
        page_count (int, if book): Number of pages
        duration (int/str, if dvd): Duration in minutes

    Returns:
        201: New item JSON representation
        400: Bad Request if validation fails
    """
    if not request.is_json:
        return error_response("Request body must be JSON.", 400)

    data: Dict[str, Any] = request.get_json() or {}

    title = data.get("title")
    author = data.get("author")
    item_type = str(data.get("type", "")).strip().lower()

    if not title or not isinstance(title, str) or not title.strip():
        return error_response("Field 'title' is required and must be non-empty.", 400)

    if not author or not isinstance(author, str) or not author.strip():
        return error_response("Field 'author' is required and must be non-empty.", 400)

    title = title.strip()
    author = author.strip()

    if item_type == "book":
        page_count = data.get("page_count")
        if page_count is None:
            return error_response("Field 'page_count' is required for Book.", 400)
        try:
            page_count_int = int(page_count)
            if page_count_int <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            return error_response("Field 'page_count' must be a positive integer.", 400)

        new_item = Book(title=title, author=author, page_count=page_count_int)

    elif item_type == "dvd":
        duration = data.get("duration")
        if duration is None:
            return error_response("Field 'duration' is required for DVD.", 400)
        try:
            duration_val = int(duration)
            if duration_val <= 0:
                raise ValueError()
        except (ValueError, TypeError):
            duration_val = duration

        new_item = DVD(title=title, author=author, duration=duration_val)

    else:
        return error_response("Invalid 'type'. Must be 'book' or 'dvd'.", 400)

    library.add_item(new_item)
    return jsonify(new_item.to_dict()), 201


@app.route("/api/items", methods=["GET"])
def list_items():
    """List collection items with optional query filters.

    Query parameters:
        available: 'true' or 'false'
        type: 'book' or 'dvd'

    Returns:
        200: List of items matching filters
        400: Bad filter query parameter
    """
    available_param = request.args.get("available")
    type_param = request.args.get("type")

    available_filter = None
    if available_param is not None:
        avail_lower = available_param.strip().lower()
        if avail_lower == "true":
            available_filter = True
        elif avail_lower == "false":
            available_filter = False
        else:
            return error_response("Invalid 'available' filter. Must be 'true' or 'false'.", 400)

    type_filter = None
    if type_param is not None:
        type_lower = type_param.strip().lower()
        if type_lower not in ["book", "dvd", "media_item"]:
            return error_response("Invalid 'type' filter. Must be 'book' or 'dvd'.", 400)
        type_filter = type_lower

    items = library.list_items(available=available_filter, item_type=type_filter)
    return jsonify(items), 200


@app.route("/api/items/<int:item_id>", methods=["GET"])
def get_item(item_id: int):
    """Retrieve details for a single item.

    Returns:
        200: Item JSON representation
        404: Not Found if item does not exist
    """
    try:
        item = library.get_item(item_id)
        return jsonify(item.to_dict()), 200
    except ItemNotFoundError as e:
        return error_response(str(e), 404)


@app.route("/api/items/<int:item_id>", methods=["PUT"])
def replace_item(item_id: int):
    """Replace all editable fields of an item.

    For Book: requires title, author, page_count
    For DVD: requires title, author, duration

    Returns:
        200: Updated item JSON
        400: Missing fields or invalid values
        404: Item not found
    """
    if not request.is_json:
        return error_response("Request body must be JSON.", 400)

    try:
        item = library.get_item(item_id)
    except ItemNotFoundError as e:
        return error_response(str(e), 404)

    data: Dict[str, Any] = request.get_json() or {}

    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        return error_response("Fields 'title' and 'author' are required.", 400)

    try:
        if isinstance(item, Book):
            page_count = data.get("page_count")
            if page_count is None:
                return error_response("Field 'page_count' is required for Book.", 400)
            try:
                page_count_int = int(page_count)
                if page_count_int <= 0:
                    raise ValueError()
            except (ValueError, TypeError):
                return error_response("Field 'page_count' must be a positive integer.", 400)

            library.update_item(
                item_id, title=title.strip(), author=author.strip(), page_count=page_count_int
            )

        elif isinstance(item, DVD):
            duration = data.get("duration")
            if duration is None:
                return error_response("Field 'duration' is required for DVD.", 400)
            try:
                duration_val = int(duration)
                if duration_val <= 0:
                    raise ValueError()
            except (ValueError, TypeError):
                duration_val = duration

            library.update_item(
                item_id, title=title.strip(), author=author.strip(), duration=duration_val
            )

        return jsonify(item.to_dict()), 200

    except ValueError as e:
        return error_response(str(e), 400)


@app.route("/api/items/<int:item_id>", methods=["PATCH"])
def update_item_partial(item_id: int):
    """Partially update editable fields of an item.

    Returns:
        200: Updated item JSON
        400: Invalid fields or attempts to modify restricted attributes
        404: Item not found
    """
    if not request.is_json:
        return error_response("Request body must be JSON.", 400)

    data: Dict[str, Any] = request.get_json() or {}
    if not data:
        return error_response("No update fields provided.", 400)

    # Validate page_count / duration if present in patch payload
    if "page_count" in data:
        try:
            page_count_int = int(data["page_count"])
            if page_count_int <= 0:
                raise ValueError()
            data["page_count"] = page_count_int
        except (ValueError, TypeError):
            return error_response("Field 'page_count' must be a positive integer.", 400)

    if "duration" in data:
        try:
            duration_val = int(data["duration"])
            if duration_val <= 0:
                raise ValueError()
            data["duration"] = duration_val
        except (ValueError, TypeError):
            pass

    try:
        updated_item = library.update_item(item_id, **data)
        return jsonify(updated_item.to_dict()), 200
    except ItemNotFoundError as e:
        return error_response(str(e), 404)
    except ValueError as e:
        return error_response(str(e), 400)


@app.route("/api/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id: int):
    """Remove an item from the library.

    Returns:
        204: Successfully deleted (no content)
        404: Item not found
        409: Item is currently checked out
    """
    try:
        library.remove_item(item_id)
        return ("", 204)
    except ItemNotFoundError as e:
        return error_response(str(e), 404)
    except ItemStateError as e:
        return error_response(str(e), 409)


@app.route("/api/items/<int:item_id>/checkout", methods=["POST"])
def checkout_item(item_id: int):
    """Check out an item from the library.

    Returns:
        200: Successfully checked out
        404: Item not found
        409: Item is already checked out
    """
    try:
        item = library.get_item(item_id)
        message = item.checkout()
        return jsonify({"message": message, "item": item.to_dict()}), 200
    except ItemNotFoundError as e:
        return error_response(str(e), 404)
    except ItemStateError as e:
        return error_response(str(e), 409)


@app.route("/api/items/<int:item_id>/return", methods=["POST"])
def return_item(item_id: int):
    """Return a checked-out item to the library.

    Returns:
        200: Successfully returned
        404: Item not found
        409: Item is not currently checked out
    """
    try:
        item = library.get_item(item_id)
        message = item.return_item()
        return jsonify({"message": message, "item": item.to_dict()}), 200
    except ItemNotFoundError as e:
        return error_response(str(e), 404)
    except ItemStateError as e:
        return error_response(str(e), 409)


# ---------------------------------------------------------------------------
# Server Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)

