####Kuanıcı olarak benim düzeltiğim şeyler:
AI app.py ile library_app.py dosyasını karıştırdı ve direk app.py dosyasını(calculator) library uygulaması ve kodu ile değiştirdi. iyi ki yakaladım yoksa sonra video çekerken calculatora erişimde sıkıntı yaşayabilirdim. Yine inatla baika porta 5001 açtığı halde 5000 müş gibi davranmaya çalıştı. Ayrıca MCP anti gravity remote olarak desteklemiyormuş sadece professional dev sürümü ile figma'dan local MCP çalışıyormuş. Ayrıca calculator uygulaması için custom_classes dan operatinları çekmek yerine direk app.py içinde tekrar tanımlamış.


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

## Section 2 - Part 3: Flask REST API

### Prompt:
> Create library_app.py in the Week4 directory to expose our LibraryCollection from library_custom_classes.py as a REST API.
> Requirements:
> - Collection Instance & Seeding: Instantiate one LibraryCollection in library_app.py and seed it with at least 3 items (mixed Books and DVDs).
> - Endpoints & HTTP Status Codes:
>   - POST /api/items: Create a Book or DVD (201 Created / 400 Bad Request)
>   - GET /api/items: List items, support filters ?available=true/false and ?type=book/dvd (200 OK / 400 Bad Request)
>   - GET /api/items/<id>: Retrieve single item (200 OK / 404 Not Found)
>   - PUT /api/items/<id>: Replace all editable fields (200 OK / 400 / 404)
>   - PATCH /api/items/<id>: Update partial editable fields (200 OK / 400 / 404)
>   - DELETE /api/items/<id>: Remove an item (204 No Content / 404 / 409 if checked out)
>   - POST /api/items/<id>/checkout: Checkout item (200 OK / 404 / 409 already out)
>   - POST /api/items/<id>/return: Return item (200 OK / 404 / 409 not checked out)
> - Error Response Format: Every error must return {"error": "<message>"} with the matching HTTP status code.
> - Dependencies: Create requirements.txt containing flask.

### Implementation Details:
- `library_app.py`: Created the Flask application with all 8 REST endpoints, input validation, clean exception translation to HTTP error codes (400, 404, 409), and 4 seeded items (2 Books, 2 DVDs).
- `requirements.txt`: Created with `flask>=3.0.0`.
- Verified all endpoints using automated test client.


## Section 2 - Part 4: Vibe-Code the Frontend and Connect It

### Prompt:
> lets move to part 4 Vibe-code the frontend and connect it.( be sure not to mess up the calculator app! the file says "flask must serve index.html, style.css, script.js." but you can change the files names to like etc library_index.html in order to be sure that we dont mess up our calculator!)
> read the week4 assignment pdf and the section with part 4. Here are the figma frame links.Fetch layout and styling directly from the Figma links below using MCP.
> Main Dashboard: https://www.figma.com/design/nB3dRsvIhceJ4pPq9PpUUN/Checkout_UI?node-id=3-1864&t=wRGIK2PgN6Q9VBBl-4
> Add Item Modal: https://www.figma.com/design/nB3dRsvIhceJ4pPq9PpUUN/Checkout_UI?node-id=3-1380&t=wRGIK2PgN6Q9VBBl-4
> Edit Item Modal: https://www.figma.com/design/nB3dRsvIhceJ4pPq9PpUUN/Checkout_UI?node-id=3-1466&t=wRGIK2PgN6Q9VBBl-4
> Empty State: https://www.figma.com/design/nB3dRsvIhceJ4pPq9PpUUN/Checkout_UI?node-id=3-1577&t=wRGIK2PgN6Q9VBBl-4
> Item Card Component: https://www.figma.com/design/nB3dRsvIhceJ4pPq9PpUUN/Checkout_UI?node-id=3-1688&t=wRGIK2PgN6Q9VBBl-4

### Generated & Updated Files:
- `library_index.html`: Complete single-page app layout with toolbar, segmented controls (All/Books/DVDs), toggle switch (Available Only), alert error banner, items card grid, empty state, and Add/Edit modal dialog.
- `library_style.css`: Clean pixel-perfect styling matching Figma color palette (`#f4f6f8` background, `#303469` primary navy, `#444d5b` modal background, badge pills, responsive cards grid).
- `library_script.js`: Complete asynchronous client communicating with all 8 REST endpoints, rendering dynamic card variants (Available / Checked Out), handling modal transitions, and displaying API error messages (especially HTTP 409).
- `library_app.py`: Configured to serve `library_index.html`, `library_style.css`, and `library_script.js` directly on route `/`.

### Corrections & Refinements (Required by Rubric):
1. **Isolated Frontend Assets from Calculator**: Prevented overwriting the calculator's `index.html`, `style.css`, and `script.js` by explicitly scoping library frontend files as `library_index.html`, `library_style.css`, and `library_script.js`.
2. **HTTP 409 Conflict Error Display**: Ensured that when attempting to delete a checked-out item (or performing an invalid checkout/return), the client catches the HTTP 409 response and renders the error message directly into the top red alert banner instead of silently failing or using an alert() popup.
3. **Dynamic Form Switching & Field Immutability**: Configured the modal form to dynamically toggle between "Page Count" and "Duration (mins)" based on media type, and disabled the type selector during Edit mode to adhere to model immutability rules.