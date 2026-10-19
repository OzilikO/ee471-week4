# Prompts Log - EE471 Week 4

## Section 1 - Part 2: Calculator Frontend & Backend Preparation

### Prompt:
> generate the front-end code (HTML, CSS, and JS) to exactly match the visual layout of the calculator in path D:\EE\EE471-week4\ee471-week4\design\Figma_calculator.png. Save the files: Create index.html, style.css, and script.js inside the ee471-week4. Keep in mind the assignment pdf at path D:\EE\EE471-week4\ee471-week4\Week-4-InClass-Exercise.pdf.

### Generated Files:
- `index.html`: Exact 4x4 calculator structure with 508px display and 16 buttons.
- `style.css`: Pixel-perfect match of the Figma design (540px width, 652px height, `#0075c9` frame background, `#ffffff` 120px display, `#90999d` 106x96px buttons with 28px/26px gaps, and `#005b9b` for the equals button).
- `script.js`: Interactive frontend supporting input digits, decimal, operators (`+`, `-`, `*`, `/`), keyboard shortcuts, display clearing, and communication with the Flask backend endpoint `POST /api/calculate`.

### Prompt 2 (Step 2 - Backend Calculation Delegation):
> In the script.js file, do not perform the mathematical calculations locally. Instead, capture the user's input and send the two numbers and the operator to a backend via a POST /api/calculate request using JSON format. Handle the response by displaying the returned result on the calculator screen. If the API returns an error message for invalid input or division by zero, display that error on the screen instead.

### Corrections & Adjustments:
1. Removed `calculateLocal` fallback from `script.js` so all computations are strictly processed by the Flask server via `POST /api/calculate`.
2. Ensured payload format exactly matches Flask expectations (`{"num1": num1, "num2": num2, "operator": operator}`).
3. Handled API error responses (HTTP 400 with `{"error": "<message>"}`) to display messages such as `"Cannot divide by zero."` directly on the screen.
4. Adjusted `.display.error-text` in `style.css` so error messages fit without truncation.

## Section 2 - Part 2: Extend the Classes with CRUD Methods

### Prompt:
> Update library_custom_classes.py and library_main.py in the Week4 folder according to these exact CRUD requirements:
> 1. Custom Exceptions: ItemNotFoundError, ItemStateError
> 2. Auto-Incrementing IDs: assigned by add_item() (1, 2, 3, ...) and never reused
> 3. Dictionary Serialization: to_dict() in MediaItem, Book (page_count), DVD (duration)
> 4. Exception-Based State Transitions: checkout() raises ItemStateError if already out; return_item() raises ItemStateError if not out; DVD.checkout() returns reminder string without printing
> 5. New Collection Methods: get_item(), list_items(available=None, item_type=None), update_item(item_id, **fields), remove_item(item_id)
> 6. Test Suite: in library_main.py demonstrate every method and catch each exception.

### Implementation Details:
- `library_custom_classes.py`: Complete OOP domain model with custom exceptions, CRUD methods, strict validation on editable fields, sequential non-reusable IDs, and dictionary serialization.
- `library_main.py`: Test suite verifying every operation and catching `ItemNotFoundError`, `ItemStateError`, and `ValueError`.