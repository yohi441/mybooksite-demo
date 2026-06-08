import re
import json
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com"
CATALOGUE_URL = f"{BASE_URL}/catalogue"

RATING_MAP = {
    "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5,
}

def parse_price(text):
    return re.sub(r'[^\d.]', '', text)

def parse_quantity(text):
    m = re.search(r'(\d+)', text)
    return int(m.group(1)) if m else 1

def get_soup(url):
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return BeautifulSoup(resp.text, 'html.parser')

def scrape_book_detail(url):
    soup = get_soup(url)
    desc_tag = soup.select_one("#product_description ~ p")
    description = desc_tag.get_text(strip=True) if desc_tag else ""

    stock_tag = soup.select_one(".instock.availability")
    quantity = parse_quantity(stock_tag.get_text()) if stock_tag else 1

    breadcrumbs = soup.select(".breadcrumb li a")
    category = breadcrumbs[-1].get_text(strip=True) if len(breadcrumbs) >= 2 else "Uncategorized"

    return description, quantity, category

books_data = []
categories = {}

page = 1
url = f"{CATALOGUE_URL}/page-{page}.html"
soup = get_soup(url)
articles = soup.select("article.product_pod")

print(f"Scraping page {page} — found {len(articles)} books")

pk = 1
for article in articles:
    title = article.h3.a["title"]
    price = parse_price(article.select_one(".price_color").get_text())
    rating_class = article.select_one(".star-rating")["class"][1]
    rating = RATING_MAP.get(rating_class, 1)
    rel_path = article.h3.a["href"]
    detail_url = f"{CATALOGUE_URL}/{rel_path}"

    print(f"  Fetching: {title}")
    description, quantity, category = scrape_book_detail(detail_url)

    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    books_data.append({
        "model": "mybooksite.book",
        "pk": pk,
        "fields": {
            "title": title,
            "price": price,
            "rating": rating,
            "description": description[:2000],
            "quantity": quantity,
            "created_at": now,
            "updated_at": now,
        },
    })

    if category not in categories:
        categories[category] = []
    categories[category].append(pk)

    pk += 1

output = list(books_data)
cat_pk = 1
for cat_name, book_pks in categories.items():
    output.append({
        "model": "mybooksite.category",
        "pk": cat_pk,
        "fields": {
            "name": cat_name,
            "books": book_pks,
        },
    })
    cat_pk += 1

fixture_path = "mybooksite/fixtures/books.json"
with open(fixture_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\nDone! {len(books_data)} books and {len(categories)} categories written to {fixture_path}")
