/**
 * Library Management System - Frontend Controller
 * Connects directly to Flask REST API endpoints:
 *   - GET    /api/items
 *   - POST   /api/items
 *   - GET    /api/items/<id>
 *   - PUT    /api/items/<id>
 *   - DELETE /api/items/<id>
 *   - POST   /api/items/<id>/checkout
 *   - POST   /api/items/<id>/return
 */

// Application State
let libraryItems = [];
let currentTypeFilter = 'all';
let availableOnly = false;
let editingItemId = null;

// DOM Elements
const itemsGrid = document.getElementById('itemsGrid');
const emptyState = document.getElementById('emptyState');
const itemsCount = document.getElementById('itemsCount');
const availableToggle = document.getElementById('availableToggle');
const segmentBtns = document.querySelectorAll('.segment-btn');
const alertBanner = document.getElementById('alertBanner');
const alertMessage = document.getElementById('alertMessage');
const dismissAlertBtn = document.getElementById('dismissAlertBtn');
const openAddModalBtn = document.getElementById('openAddModalBtn');
const emptyAddBtn = document.getElementById('emptyAddBtn');
const itemModal = document.getElementById('itemModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelModalBtn = document.getElementById('cancelModalBtn');
const itemForm = document.getElementById('itemForm');
const modalTitle = document.getElementById('modalTitle');
const modalItemId = document.getElementById('modalItemId');
const itemTitleInput = document.getElementById('itemTitleInput');
const itemAuthorInput = document.getElementById('itemAuthorInput');
const itemTypeSelect = document.getElementById('itemTypeSelect');
const dynamicFieldLabel = document.getElementById('dynamicFieldLabel');
const itemDynamicInput = document.getElementById('itemDynamicInput');

/**
 * Display error banner with custom message from API
 */
function showAlert(message) {
  alertMessage.textContent = message || 'An unexpected error occurred.';
  alertBanner.style.display = 'flex';
}

/**
 * Dismiss/hide error banner
 */
function hideAlert() {
  alertBanner.style.display = 'none';
}

/**
 * Updates dynamic field label and placeholder based on media type
 */
function updateDynamicField(type, value = '') {
  if (type === 'dvd') {
    dynamicFieldLabel.textContent = 'Duration (mins)';
    itemDynamicInput.placeholder = '148';
  } else {
    dynamicFieldLabel.textContent = 'Page Count';
    itemDynamicInput.placeholder = '220';
  }
  itemDynamicInput.value = value !== undefined && value !== null ? value : '';
}

/**
 * Fetches items from Flask API applying current filters
 */
async function fetchItems() {
  try {
    const params = new URLSearchParams();
    if (availableOnly) {
      params.append('available', 'true');
    }
    if (currentTypeFilter !== 'all') {
      params.append('type', currentTypeFilter);
    }

    const queryString = params.toString() ? `?${params.toString()}` : '';
    const response = await fetch(`/api/items${queryString}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to load items.');
    }

    libraryItems = data;
    renderItems();
  } catch (err) {
    showAlert(err.message);
  }
}

/**
 * Renders item cards into grid or displays empty state
 */
function renderItems() {
  itemsCount.textContent = `${libraryItems.length} item${libraryItems.length === 1 ? '' : 's'}`;

  if (!libraryItems || libraryItems.length === 0) {
    itemsGrid.style.display = 'none';
    emptyState.style.display = 'flex';
    itemsGrid.innerHTML = '';
    return;
  }

  emptyState.style.display = 'none';
  itemsGrid.style.display = 'grid';

  itemsGrid.innerHTML = libraryItems.map(item => {
    const isBook = item.type === 'book';
    const detailText = isBook 
      ? `${item.page_count} pages` 
      : `${item.duration} mins`;

    const statusBadge = item.is_available
      ? `<div class="status-badge available"><span class="status-dot"></span>Available</div>`
      : `<div class="status-badge checked-out"><span class="status-dot"></span>Checked Out</div>`;

    const actionButton = item.is_available
      ? `<button type="button" class="btn btn-checkout" data-action="checkout" data-id="${item.id}">Checkout</button>`
      : `<button type="button" class="btn btn-return" data-action="return" data-id="${item.id}">Return</button>`;

    return `
      <article class="item-card" data-id="${item.id}">
        <h3 class="card-title">${escapeHtml(item.title)}</h3>
        <p class="card-author">${escapeHtml(item.author)}</p>
        
        <div class="card-meta-row">
          <span class="type-pill">${escapeHtml(item.type)}</span>
          <span class="detail-text">${escapeHtml(detailText)}</span>
        </div>

        ${statusBadge}

        <div class="card-actions">
          ${actionButton}
          <div class="icon-actions">
            <button type="button" class="btn-icon-action btn-icon-edit" data-action="edit" data-id="${item.id}" title="Edit Item" aria-label="Edit Item">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </button>
            <button type="button" class="btn-icon-action btn-icon-delete" data-action="delete" data-id="${item.id}" title="Delete Item" aria-label="Delete Item">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="3 6 5 6 21 6"></polyline>
                <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
              </svg>
            </button>
          </div>
        </div>
      </article>
    `;
  }).join('');
}

/**
 * Escapes HTML characters to prevent XSS
 */
function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Checkout an item via POST /api/items/<id>/checkout
 */
async function handleCheckout(id) {
  try {
    const response = await fetch(`/api/items/${id}/checkout`, { method: 'POST' });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to checkout item.');
    }

    hideAlert();
    await fetchItems();
  } catch (err) {
    showAlert(err.message);
  }
}

/**
 * Return an item via POST /api/items/<id>/return
 */
async function handleReturn(id) {
  try {
    const response = await fetch(`/api/items/${id}/return`, { method: 'POST' });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to return item.');
    }

    hideAlert();
    await fetchItems();
  } catch (err) {
    showAlert(err.message);
  }
}

/**
 * Delete an item via DELETE /api/items/<id>
 * Displays the 409 error banner if item is checked out!
 */
async function handleDelete(id) {
  try {
    const response = await fetch(`/api/items/${id}`, { method: 'DELETE' });

    if (response.status === 204) {
      hideAlert();
      await fetchItems();
      return;
    }

    const data = await response.json();
    throw new Error(data.error || 'Cannot delete item.');
  } catch (err) {
    // Displays the API error (e.g. 409 message "Cannot remove checked-out item #...")
    showAlert(err.message);
  }
}

/**
 * Open Modal in "Add New Item" mode
 */
function openAddModal() {
  editingItemId = null;
  modalTitle.textContent = 'Add New Item';
  modalItemId.value = '';
  itemTitleInput.value = '';
  itemAuthorInput.value = '';
  itemTypeSelect.value = 'book';
  itemTypeSelect.disabled = false;
  updateDynamicField('book');
  itemModal.style.display = 'flex';
  itemTitleInput.focus();
}

/**
 * Open Modal in "Edit Item" mode
 */
function openEditModal(item) {
  editingItemId = item.id;
  modalTitle.textContent = 'Edit Item';
  modalItemId.value = item.id;
  itemTitleInput.value = item.title;
  itemAuthorInput.value = item.author;
  itemTypeSelect.value = item.type;
  itemTypeSelect.disabled = true; // Type cannot be modified per model rules

  const dynamicVal = item.type === 'book' ? item.page_count : item.duration;
  updateDynamicField(item.type, dynamicVal);
  itemModal.style.display = 'flex';
  itemTitleInput.focus();
}

/**
 * Closes Add/Edit modal
 */
function closeModal() {
  itemModal.style.display = 'none';
  itemForm.reset();
  editingItemId = null;
  itemTypeSelect.disabled = false;
}

/**
 * Form Submission (Handles both Add POST and Edit PUT)
 */
async function handleFormSubmit(e) {
  e.preventDefault();

  const title = itemTitleInput.value.trim();
  const author = itemAuthorInput.value.trim();
  const type = itemTypeSelect.value;
  const dynamicVal = parseInt(itemDynamicInput.value, 10);

  if (!title || !author) {
    showAlert('Title and Author are required.');
    return;
  }

  if (isNaN(dynamicVal) || dynamicVal <= 0) {
    showAlert(`Please enter a valid positive number for ${type === 'book' ? 'Page Count' : 'Duration'}.`);
    return;
  }

  const payload = {
    title: title,
    author: author,
    type: type
  };

  if (type === 'book') {
    payload.page_count = dynamicVal;
  } else {
    payload.duration = dynamicVal;
  }

  try {
    let response;
    if (editingItemId) {
      // Edit existing item using PUT
      response = await fetch(`/api/items/${editingItemId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    } else {
      // Add new item using POST
      response = await fetch('/api/items', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to save item.');
    }

    closeModal();
    hideAlert();
    await fetchItems();
  } catch (err) {
    showAlert(err.message);
  }
}

// ---------------------------------------------------------------------------
// Event Listeners
// ---------------------------------------------------------------------------

// Available Only toggle switch
availableToggle.addEventListener('change', (e) => {
  availableOnly = e.target.checked;
  fetchItems();
});

// Type filter tabs (All, Books, DVDs)
segmentBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    segmentBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentTypeFilter = btn.dataset.type;
    fetchItems();
  });
});

// Dynamic field switch on media type change
itemTypeSelect.addEventListener('change', (e) => {
  updateDynamicField(e.target.value);
});

// Modal triggers
openAddModalBtn.addEventListener('click', openAddModal);
emptyAddBtn.addEventListener('click', openAddModal);
closeModalBtn.addEventListener('click', closeModal);
cancelModalBtn.addEventListener('click', closeModal);

// Close modal when clicking outside dialog
itemModal.addEventListener('click', (e) => {
  if (e.target === itemModal) {
    closeModal();
  }
});

// Form submit
itemForm.addEventListener('submit', handleFormSubmit);

// Dismiss alert banner
dismissAlertBtn.addEventListener('click', hideAlert);

// Event delegation for card actions (Checkout, Return, Edit, Delete)
itemsGrid.addEventListener('click', (e) => {
  const btn = e.target.closest('button');
  if (!btn) return;

  const action = btn.dataset.action;
  const id = parseInt(btn.dataset.id, 10);
  if (!id) return;

  if (action === 'checkout') {
    handleCheckout(id);
  } else if (action === 'return') {
    handleReturn(id);
  } else if (action === 'delete') {
    handleDelete(id);
  } else if (action === 'edit') {
    const item = libraryItems.find(it => it.id === id);
    if (item) {
      openEditModal(item);
    }
  }
});

// Initial load
fetchItems();

