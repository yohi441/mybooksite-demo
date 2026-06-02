# Mybooksite — Project Documentation

## Architecture Overview

```
config/                  # Django project config (settings, root URLs, WSGI/ASGI)
mybooksite/              # Book catalog app
accounts/                # User auth & profiles app
carts/                   # Shopping cart & orders app
templates/               # 43 Django templates (component-based architecture)
static/                  # Tailwind CSS, HTMX, Alpine.js
```

### Apps Breakdown

| App | Purpose | Models |
|---|---|---|
| `mybooksite` | Book catalog, browsing, search | `Book`, `Category` |
| `accounts` | Auth, profiles, registration, password reset | `Profile` (linked to Django's `User`) |
| `carts` | Shopping cart, checkout, order history | `Cart`, `Checkout` |

---

## Models

### `mybooksite/models.py` — Book & Category

#### Book

| Field | Type | Notes |
|---|---|---|
| `title` | `CharField(max_length=500)` | |
| `price` | `DecimalField(max_digits=5, decimal_places=2)` | |
| `rating` | `PositiveIntegerField(choices=1-5)` | |
| `description` | `TextField(max_length=2000)` | |
| `img` | `ImageField(upload_to="book_img/")` | Nullable |
| `quantity` | `PositiveIntegerField(default=1)` | Used for stock check |
| `created_at` | `DateTimeField(auto_now_add=True)` | |
| `updated_at` | `DateTimeField(auto_now=True)` | |

**Property**: `is_in_stock` — returns `'in stock'` if `quantity > 0`, else `'out of stock'`.

**Note**: There's a commented-out `thumbnail` ImageField in the model. The signal `mybooksite/signals.py` still writes to it via `instance.thumbnail.save(...)`, but the signal import in `apps.py` is commented out, so thumbnails are NOT generated currently. If you want thumbnails, uncomment the `thumbnail` field in the model and uncomment the `ready()` method in `mybooksite/apps.py`.

#### Category

| Field | Type | Notes |
|---|---|---|
| `name` | `CharField(max_length=100)` | |
| `books` | `ManyToManyField(Book, related_name="categories")` | Blank allowed |

`Meta.verbose_name_plural = "Categories"`

---

### `accounts/models.py` — Profile

| Field | Type | Notes |
|---|---|---|
| `user` | `OneToOneField(User, on_delete=CASCADE)` | Linked to Django auth User |
| `avatar` | `ImageField(upload_to="avatar/")` | Nullable |
| `address` | `CharField(max_length=100)` | Nullable |
| `cellphone_number` | `PositiveIntegerField` | Nullable |
| `gender` | `CharField(choices=Male/Female/Other)` | Nullable |
| `created_at` | `DateTimeField(auto_now_add=True)` | |
| `updated_at` | `DateTimeField(auto_now=True)` | |

Auto-created via signal when a new `User` is saved.

---

### `carts/models.py` — Cart & Checkout

#### Cart

| Field | Type | Notes |
|---|---|---|
| `user` | `OneToOneField(User, on_delete=CASCADE)` | One cart per user |
| `books` | `ManyToManyField(Book)` | Blank allowed |
| `created_at` | `DateTimeField(auto_now_add=True)` | |
| `update_at` | `DateTimeField(auto_now=True)` | |

Auto-created via signal when a new `User` is saved.

#### Checkout (an order)

| Field | Type | Notes |
|---|---|---|
| `user` | `ForeignKey(User, on_delete=CASCADE)` | User who placed the order |
| `books` | `ManyToManyField(Book)` | Books ordered |
| `total` | `DecimalField(max_digits=100, decimal_places=2, default=0.00)` | |
| `created_at` | `DateTimeField(auto_now_add=True)` | |
| `updated_at` | `DateTimeField(auto_now=True)` | |

---

## Signals

### `accounts/signals.py` — Create Profile on User signup

```python
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

### `carts/signals.py` — Create Cart on User signup

```python
@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
```

### `mybooksite/signals.py` — Book thumbnail generation (DISABLED)

```python
@receiver(pre_save, sender=Book)
def create_thumbnail(sender, instance, **kwargs):
    if instance.img:
        img = Image.open(instance.img)
        img.thumbnail((200, 200), Image.ANTIALIAS)
        temp_thumb = BytesIO()
        img.save(temp_thumb, "JPEG")
        temp_thumb.seek(0)
        instance.thumbnail.save(instance.img.name, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()
```

**Status**: The `ready()` method in `mybooksite/apps.py` is commented out, so this signal is NOT active. The `Book.thumbnail` field is also commented out in the model. To enable: uncomment the `thumbnail` field in the model, run `makemigrations` + `migrate`, then uncomment `ready()` in `apps.py`.

---

## Views & Features

### 1. Book Catalog (`mybooksite/views.py`)

#### IndexView — Home page with book listing
- **URL**: `/` — name: `mybooksite:index`
- **Type**: `ListView`
- **Template**: `index.html`
- **Pagination**: 10 books per page, ordered by `updated_at`
- **Context**: `categories` (all), `count` (cart items), `mylist` (static list 1-5 — used for rating stars display)

#### BookDetailView — Single book page
- **URL**: `/book-detail/<pk>` — name: `mybooksite:detail`
- **Type**: `DetailView`
- **Template**: `detail.html`
- **Recently Viewed**: Tracks up to 5 recently viewed books in session (`request.session['recently_viewed']`). Maintains order — newest first, removes duplicates, capped at 5.
- **Context**: `count`, `recently_viewed_book` (queried and sorted by session order), `book`

#### SearchView — Live search via HTMX
- **URL**: `/search/?q=` — name: `mybooksite:search`
- **Type**: `View` (GET only)
- **Template**: `components/search_results.html`
- **Logic**: Searches `Book.title__icontains`, returns top 10 results. If query is empty, shows "Search field is empty" message.
- **HTMX behavior**: This endpoint is called via HTMX from `components/search.html` — returns only the results partial (no full page reload).

#### CategoryView — Filter by category
- **URL**: `/category/<pk>` — name: `mybooksite:category`
- **Type**: `View` (GET only)
- **Template**: `index.html` (reuses the same template as IndexView)
- **Logic**: Gets category by pk, filters that category's books, paginates by 10.
- **Context**: `categories`, `count`, `page_obj`

#### AboutUsView — Static about page
- **URL**: `/about-us/` — name: `mybooksite:about_us`
- **Type**: `TemplateView`
- **Template**: `about_us.html`
- **Context**: `count`

---

### 2. Authentication & Accounts (`accounts/views.py`)

#### MyLoginView — User login
- **URL**: `/accounts/login/` — name: `accounts:login`
- **Type**: `View` (GET/POST)
- **Template**: `accounts/login.html`
- **Logic**: Uses Django's `AuthenticationForm`. If user is already authenticated, redirects to `/`. On POST with valid form, logs in and redirects to `/`.

#### MyLogoutView — User logout
- **URL**: `/accounts/logout/` — name: `accounts:logout`
- **Type**: `View` (GET only)
- **Logic**: Calls `logout(request)`, then redirects to `mybooksite:index`.

#### MyRegisterView — User registration
- **URL**: `/accounts/register/` — name: `accounts:register`
- **Type**: `View` (GET/POST)
- **Template**: `accounts/register.html`
- **Form**: `RegisterForm` (extends `UserCreationForm` — adds `email` field, sets `username` min_length=4, max_length=10)
- **Logic**: On valid submission saves the user, redirects to `accounts:register_success`.

#### RegisterSuccess — Registration confirmation
- **URL**: `/accounts/register-success/` — name: `accounts:register_success`
- **Type**: `View` (GET only)
- **Template**: `register_success.html`

#### CheckUsername — HTMX username validation
- **URL**: `/accounts/check-username/` — name: `accounts:check_username`
- **Type**: `View` (POST only from HTMX)
- **Template**: `accounts/partials/invalid_username.html`
- **Logic**: Checks if username >= 4 chars, checks if already exists. Returns partial with message and color class.

#### CheckEmail — HTMX email validation
- **URL**: `/accounts/check-email/` — name: `accounts:check_email`
- **Type**: `View` (POST only from HTMX)
- **Templates**: 
  - Valid: `accounts/partials/valid_email.html`
  - Invalid: `accounts/partials/invalid_email.html`
  - Empty: `accounts/partials/invalid_email_field_required.html`
- **Logic**: Validates email format via regex.

#### ProfileView — User profile page
- **URL**: `/accounts/profile/` — name: `accounts:profile`
- **Type**: `View` (GET, LoginRequired)
- **Template**: `profile.html`
- **Context**: `count`

#### ProfileEdit — Edit profile (HTMX enabled)
- **URL**: `/accounts/edit-profile` — name: `accounts:edit_profile`
- **Type**: `View` (GET/POST)
- **Templates**: 
  - HTMX request: `accounts/partials/edit_profile.html` (partial)
  - Full page: `accounts/edit_profile_full.html`
- **Form**: `ProfileForm` (ModelForm for `Profile`)
- **Logic**: On POST, saves both `Profile` fields and `User` fields (first_name, last_name, email). The `Profile` fields in the form are: address, gender, cellphone_number, avatar. The `User` fields are mapped manually from cleaned_data.

#### PasswordResetRequest — Custom password reset
- **URL**: `/accounts/password-reset/` — name: `accounts:password_reset`
- **Type**: `View` (GET/POST)
- **Template**: `accounts/password_reset.html`
- **Logic**: Uses Django's `PasswordResetForm`. Sends email with token. Domain and protocol are derived dynamically from `request.get_host()` and `request.scheme`.
- **Built-in views used**:
  - `PasswordChangeView` — URL: `password-change/`, template: `accounts/password_change.html`
  - `PasswordChangeDoneView` — URL: `password-change-done/`, template: `accounts/password_change_done.html`
  - `PasswordResetDoneView` — URL: `password-reset-done/`, template: `accounts/password_reset_done.html`
  - `PasswordResetConfirmView` — URL: `password-reset-confirm/<uidb64>/<token>/`, template: `accounts/password_reset_confirm.html`, success_url: `password_reset_complete`
  - `PasswordResetCompleteView` — URL: `password-reset-complete/`, template: `accounts/password_reset_complete.html`

---

### 3. Shopping Cart & Orders (`carts/views.py`)

#### Helper Functions

**`get_count_cart(request)`**: Returns number of books in user's cart (0 if unauthenticated). Used across all apps for the cart badge.

**`get_items_in_cart(cart)`**: Returns a list of book IDs in the cart.

#### CartView — View cart contents
- **URL**: `/carts/` — name: `carts:cart`
- **Type**: `View` (GET, LoginRequired)
- **Template**: `carts/cart.html`
- **Context**: `cart`, `count`, `item_in_cart` (list of book IDs)

#### AddToCart — Add a book to cart (HTMX)
- **URL**: `/carts/add-to-cart/<pk>/` — name: `carts:add_to_cart`
- **Type**: `View` (POST only)
- **Response templates** (partials):
  - Success: `carts/partials/add_to_cart_alert.html` — shows `new_count` (updated cart count)
  - Already in cart: `carts/partials/add_to_cart_book_exist.html`
  - Out of stock: `carts/partials/add_to_cart_book_out_of_stock.html`
  - Error: `carts/partials/add_to_cart_book_error.html`
- **Logic**: Checks if book is in stock, checks if book already in cart, then adds.

#### CartItemDelete — Remove a book from cart (HTMX)
- **URL**: `/carts/cart-item-delete/<pk>/` — name: `carts:cart_item_delete`
- **Type**: `View` (DELETE/GET)
- **Template**: `carts/partials/partial_cart.html`
- **Logic**: Removes book from cart, returns updated cart partial with `new_count`.

#### CheckboxCheck — Checkout summary
- **URL**: `/carts/checkout/` — name: `carts:checkout`
- **Type**: `View` (POST, LoginRequired)
- **Template**: `carts/checkout.html`
- **Logic**: Receives list of book IDs from cart checkboxes, displays them with total price.

#### RecentOrder — Place/view an order
- **URL**: `/carts/recent-order/` — name: `carts:recent_order`
- **Type**: `View` (GET/POST, LoginRequired)
- **Template**: `carts/recent_order.html`
- **POST logic**: Creates a new `Checkout` instance, adds selected books, calculates total, saves.
- **GET logic**: Shows the most recent order for the user.

#### ListOfOrders — View all orders
- **URL**: `/carts/orders/` — name: `carts:orders`
- **Type**: `View` (GET, LoginRequired)
- **Template**: `carts/orders.html`
- **Context**: `user_orders` (all orders for the user, newest first), `count`

#### DetailOrder — View a single order
- **URL**: `/carts/order-detail/<pk>/` — name: `carts:detail_order`
- **Type**: `View` (GET, LoginRequired)
- **Template**: `carts/list_of_order.html`
- **Context**: `recent_order`, `list_of_books`, `total`, `count`

#### DeleteOrder — Delete an order (HTMX)
- **URL**: `/carts/delete-order/<pk>/` — name: `carts:delete_order`
- **Type**: `View` (DELETE, LoginRequired)
- **Template**: `carts/partials/partial_order.html`
- **Logic**: Deletes the order, returns updated order list partial.

---

## URL Structure

### Root (`config/urls.py`)
```
/admin/              → Django admin (site header: "BOOKSITE Admin")
/                    → mybooksite.urls (catalog)
/accounts/           → accounts.urls (auth)
/carts/              → carts.urls (cart/orders)
```

### `mybooksite/urls.py`
```
/                              → IndexView        [index]
/search/                       → SearchView        [search]
/book-detail/<pk>              → BookDetailView    [detail]
/category/<pk>                 → CategoryView      [category]
/about-us/                     → AboutUsView       [about_us]
```

### `accounts/urls.py`
```
/profile/                      → ProfileView       [profile]
/login/                        → MyLoginView       [login]
/logout/                       → MyLogoutView      [logout]
/register/                     → MyRegisterView    [register]
/register-success/             → RegisterSuccess   [register_success]
/password-change/              → PasswordChangeView [password_change]
/password-change-done/         → PasswordChangeDoneView [password_change_done]
/password-reset/               → PasswordResetRequest [password_reset]
/password-reset-done/          → PasswordResetDoneView [password_reset_done]
/password-reset-confirm/<uidb64>/<token>/ → PasswordResetConfirmView [password_reset_confirm]
/password-reset-complete/      → PasswordResetCompleteView [password_reset_complete]

--- HTMX endpoints ---
/check-username/               → CheckUsername     [check_username]
/check-email/                  → CheckEmail        [check_email]
/edit-profile                  → ProfileEdit       [edit_profile]
```

### `carts/urls.py`
```
/                              → CartView          [cart]
/add-to-cart/<pk>/             → AddToCart         [add_to_cart]
/checkout/                     → CheckboxCheck     [checkout]
/recent-order/                 → RecentOrder       [recent_order]
/orders/                       → ListOfOrders      [orders]
/order-detail/<pk>/            → DetailOrder       [detail_order]

--- HTMX endpoints ---
/cart-item-delete/<pk>/        → CartItemDelete    [cart_item_delete]
/delete-order/<pk>/            → DeleteOrder       [delete_order]
```

---

## Forms

### `accounts/forms.py`

#### RegisterForm
- Extends Django's `UserCreationForm`
- Adds `email` field (required)
- Sets `username` with `min_length=4`, `max_length=10`
- Overrides `save()` to set the email on the user

#### ProfileForm
- `ModelForm` for `Profile` model
- Adds extra fields for `first_name`, `last_name`, `email` (these are `User` fields, not `Profile` fields)
- Fields: `first_name`, `last_name`, `email`, `address`, `gender` (RadioSelect), `cellphone_number`, `avatar`

---

## Settings (`config/settings.py`)

| Setting | Value |
|---|---|
| Framework | Django 3.2 |
| Secret Key | From env var `SECRET_KEY` via `python-decouple` |
| Debug | From env var `DEBUG` (default False) |
| Allowed Hosts | From env var `ALLOWED_HOSTS` (CSV, default `127.0.0.1`) |
| Database (Debug=True) | SQLite (`db.sqlite3`) |
| Database (Debug=False) | PostgreSQL via env vars: `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` |
| Static files | WhiteNoise `CompressedManifestStaticFilesStorage`; source: `static/`, collected to: `staticfiles/` |
| Media storage | Cloudinary (`MediaCloudinaryStorage`) via env vars: `CLOUD_NAME`, `API_KEY`, `API_SECRET` |
| Email (Debug=True) | Console backend |
| Email (Debug=False) | SMTP via env vars: `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_PORT`, `EMAIL_USE_TLS` |
| Templates | `DIRS` = `templates/` at project root |
| Timezone | UTC |
| Default auto field | `BigAutoField` |
| Login redirect | `/` |

---

## Template Architecture

```
templates/
├── base.html                         # Root template — HTMX, Alpine.js, Tailwind
├── index.html                        # Book listing (used by IndexView + CategoryView)
├── detail.html                       # Book detail page
├── about_us.html                     # About page
├── profile.html                      # User profile
├── register_success.html             # Registration confirmation
│
├── accounts/
│   ├── login.html, register.html, logout.html
│   ├── password_change.html, password_change_done.html
│   ├── password_reset.html, password_reset_done.html
│   ├── password_reset_confirm.html, password_reset_complete.html
│   ├── password_message.txt          # Plaintext email template for password reset
│   ├── edit_profile_full.html        # Full page edit profile
│   └── partials/
│       ├── edit_profile.html         # HTMX partial — profile edit form
│       ├── profile.html              # HTMX partial — profile display
│       ├── valid_email.html          # HTMX partial — email valid feedback
│       ├── invalid_email.html        # HTMX partial — email invalid feedback
│       ├── invalid_email_field_required.html  # HTMX partial — email empty
│       └── invalid_username.html     # HTMX partial — username validation
│
├── carts/
│   ├── cart.html                     # Shopping cart page
│   ├── checkout.html                 # Checkout summary
│   ├── orders.html                   # All orders list
│   ├── recent_order.html             # Order confirmation
│   ├── list_of_order.html            # Single order detail
│   └── partials/
│       ├── add_to_cart_alert.html    # HTMX toast — successfully added
│       ├── add_to_cart_book_exist.html  # HTMX toast — already in cart
│       ├── add_to_cart_book_out_of_stock.html  # HTMX toast — out of stock
│       ├── add_to_cart_book_error.html  # HTMX toast — error
│       ├── partial_cart.html         # HTMX partial — refreshed cart contents
│       └── partial_order.html        # HTMX partial — refreshed order list
│
└── components/
    ├── navbar.html, bottom_nav.html, footer.html
    ├── user_nav.html, user_nav_button.html
    ├── nav_categories.html, search.html, search_results.html
    ├── hero.html, card.html
```

### Base Template (`base.html`)
- Loads: HTMX (`static/js/htmx.js`), Alpine.js (`static/js/alpine.js`), Tailwind CSS (`static/css/style.css`)
- Alpine.js data: `{overFlow:false, xcount:{{count}}}` — manages body overflow for mobile menu and reactive cart count
- HTMX config: auto-injects CSRF token via `htmx:configRequest` event listener

### HTMX Integration Pattern
Most dynamic features follow this pattern:
1. A user action triggers an `hx-post`, `hx-delete`, or `hx-get` request
2. The server returns an HTML partial (not JSON)
3. HTMX swaps the response into the DOM at the target specified by `hx-target`

---

## Admin

| Model | Registered In | Notes |
|---|---|---|
| `Book` | `mybooksite/admin.py` | Has a `BookAdmin` with `thumbnail` as readonly; `Group` is unregistered |
| `Category` | `mybooksite/admin.py` | |
| `Profile` | `accounts/admin.py` | |
| `Cart` | `carts/admin.py` | |
| `Checkout` | `carts/admin.py` | |

Admin site customization in `config/urls.py`:
- `site_header = "BOOKSITE Admin"`
- `site_title = "BOOKSITE Admin Portal"`
- `index_title = "Welcome to BOOKSITE Portal"`

---

## Testing

### Configuration
- **Framework**: pytest 7.0 + pytest-django 4.5.2
- **Settings module**: `config.settings`
- **File pattern**: `test_*.py`
- **Coverage config** (`.coveragerc`): omits `*/test/*` and `*/migrations/*`
- **Test data**: mixer 7.2.1 + Faker 12.0.1

### Test Files

| File | What it tests |
|---|---|
| `mybooksite/tests/test_urls.py` | URL resolution for all mybooksite routes |
| `mybooksite/tests/test_views.py` | Book detail view (uses `RequestFactory` + `SessionMiddleware`) |
| `mybooksite/tests/test_models.py` | (not shown — check file) |
| `accounts/tests/test_forms.py` | ProfileForm and RegisterForm validation |
| `accounts/tests/test_urls.py` | URL resolution for accounts routes |
| `accounts/tests/test_models.py` | (not shown — check file) |
| `carts/tests/test_urls.py` | URL resolution for carts routes |
| `carts/tests/test_models.py` | (not shown — check file) |

**Run tests**: `pytest`

---

## Deployment Notes

### `runtime.txt` — Python 3.8.10
### `Procfile` — `web: gunicorn config.wsgi`

### Database
- Development: SQLite (auto)
- Production: PostgreSQL (set `DEBUG=False` and configure `DB_*` env vars)

### Static Files
```bash
python manage.py collectstatic
```
WhiteNoise serves them in production.

### Media Files
Images (book images, avatars) are stored on **Cloudinary**. Requires `CLOUD_NAME`, `API_KEY`, `API_SECRET` env vars.

### Email
- Development: prints to console
- Production: SMTP — requires `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_PORT`, `EMAIL_USE_TLS`


