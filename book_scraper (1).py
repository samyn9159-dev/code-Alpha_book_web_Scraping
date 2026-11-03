
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin
import time

url = "https://books.toscrape.com/catalogue/page-1.html"

books = []

ratings = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

while url:
    response = requests.get(url, timeout=20)
    soup = BeautifulSoup(response.text, "html.parser")

    for book in soup.select("article.product_pod"):
        title = book.h3.a["title"]

        price = book.select_one(
            ".price_color"
        ).text.replace("£", "").replace("Â", "")

        rating = ratings[
            book.select_one("p.star-rating")["class"][1]
        ]

        availability = book.select_one(
            ".availability"
        ).text.strip()

        books.append({
            "Book_Name": title,
            "Price": price,
            "Rating": rating,
            "Availability": availability
        })

    next_page = soup.select_one("li.next a")

    if next_page:
        url = urljoin(url, next_page["href"])
    else:
        url = None

    time.sleep(0.5)

df = pd.DataFrame(books)
df.to_csv("books_data.csv", index=False)

print("Scraping Completed!")
print("Total Books:", len(df))
