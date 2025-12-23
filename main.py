from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
PER_PAGE = 20py 
TOTAL_PAGES = 10  # Set max pages you want to allow

def scrape_books_for_page(page_num):
    """Scrape a single page from the website."""
    url = f"https://books.toscrape.com/catalogue/page-{page_num}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for book in soup.select(".product_pod"):
        books.append({
            "title": book.h3.a["title"],
            "price": book.select_one(".price_color").text,
            "stock": book.select_one(".instock.availability").text.strip(),
            "rating": book.p["class"][1]
        })
    return books

@app.route("/")
def home():
    return books_page(1)

@app.route("/page/<int:page_num>")
def books_page(page_num):
    if page_num < 1 or page_num > TOTAL_PAGES:
        page_num = 1  # default to page 1 if out of range

    books = scrape_books_for_page(page_num)
    return render_template(
        "index.html",
        books=books,
        page_num=page_num,
        total_pages=TOTAL_PAGES
    )

if __name__ == "__main__":
    app.run(debug=True)
