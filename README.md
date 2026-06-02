# Mybooksite

A demo e-commerce bookshop web application built with Django, HTMX, and Alpine.js.

## Features

- **Book catalog** — browse and search books by title, filter by category, paginated listing
- **Book detail** — view book info with recently-viewed tracking (up to 5 books)
- **User authentication** — register, login/logout, password reset via email, username/email validation (HTMX)
- **Profile management** — edit profile (name, email, address, phone, gender, avatar) with HTMX partial updates
- **Shopping cart** — add/remove books, stock validation, cart count badge, all with HTMX (no full page reloads)
- **Checkout & orders** — select books to purchase, place orders, view order history, delete orders via HTMX
- **HTMX-driven UX** — most dynamic interactions (cart ops, form validation, profile editing, order deletion) return HTML partials

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.8.10 |
| Framework | Django 3.2 |
| Frontend | HTMX, Alpine.js, Tailwind CSS |
| Database | PostgreSQL (production) / SQLite (development) |
| Static files | WhiteNoise |
| Media storage | Cloudinary |
| Server | Gunicorn |
| Testing | pytest, pytest-django, mixer, Faker |

## Project Structure

```
mybooksite-demo/
├── mybooksite/          # Core book catalog app
│   ├── models.py        # Book, Category
│   ├── views.py         # IndexView, BookDetailView, SearchView, CategoryView
│   ├── urls.py
│   └── signals.py       # Book thumbnail generation
├── accounts/            # User auth & profiles app
│   ├── models.py        # Profile (linked to Django auth.User)
│   ├── views.py         # Login, Register, Profile, Password reset, HTMX validation endpoints
│   ├── urls.py
│   └── forms.py
├── carts/               # Shopping cart & orders app
│   ├── models.py        # Cart, Checkout
│   ├── views.py         # CartView, AddToCart, Checkout, Orders, HTMX delete endpoints
│   └── urls.py
├── config/              # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
├── templates/           # Django templates (43 files, component-based with partials)
├── static/              # Tailwind CSS, HTMX, Alpine.js
├── manage.py
├── requirements.txt
├── runtime.txt          # python-3.8.10
└── pytest.ini
```

## Getting Started

### Prerequisites

- Python 3.8.10
- pip

### Setup

```bash
git clone <repo-url>
cd mybooksite-demo
python -m venv venv
source venv/bin/activate     # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Optional for media (Cloudinary):

```env
CLOUD_NAME=your-cloud-name
API_KEY=your-api-key
API_SECRET=your-api-secret
```

Optional for PostgreSQL (defaults to SQLite when `DEBUG=True`):

```env
DB_NAME=mybooksite
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
```

### Run

```bash
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`.

### Load sample data

```bash
python manage.py loaddata fixtures.json   # if available, or use admin panel
```

### Testing

```bash
pytest
```

## License

This project is for demonstration purposes only. The book data is dummy content scraped from the internet.
