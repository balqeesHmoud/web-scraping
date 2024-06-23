import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_URL = os.getenv('URL')

# Function to get book details from a single category
def get_books_from_category(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    books = []
    for book in soup.select('.product_pod'):
        title = book.h3.a['title']
        rating = book.p['class'][1]  # Get the second class name which is the rating
        price = book.select_one('.price_color').text
        availability = book.select_one('.availability').text.strip()

        books.append({
            "title": title,
            "rating": rating,
            "price": price,
            "availability": availability
        })

    return books

# Main function to scrape books from multiple categories
def scrape_books():
    categories = [
        'travel_2/index.html',
        'mystery_3/index.html',
        'historical-fiction_4/index.html'
    ]

    result = []

    for category in categories:
        category_url = BASE_URL + 'catalogue/category/books/' + category
        category_name = category.split('/')[0].replace('-', ' ').title()
        books = get_books_from_category(category_url)
        result.append({
            "data": books,
            "type": category_name
        })

    # Save the result to a JSON file
    with open('book_api.json', 'w') as json_file:
        json.dump(result, json_file, indent=4)

# Run the scraper
if __name__ == "__main__":
    scrape_books()
