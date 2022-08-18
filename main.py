#! /usr/bin/env python3
# coding: utf-8

import os
import csv
import urllib
import argparse

import requests
from bs4 import BeautifulSoup as BS

URL = "http://books.toscrape.com/"
URL_CATALOG = "http://books.toscrape.com/catalogue/"
VERBOSE = False

ratings = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
}


def display_category(category):
    """Display categories if verbose"""
    if VERBOSE:
        print(f"{category['name'].upper():<20}: {category['index']}")
        print(category['books'])
        print(f"Number of books: {len(category['books'])}")
        print("\n")


def get_soup(url="http://books.toscrape.com/"):
    """get a soup"""
    page = requests.get(url)
    soup = BS(page.content, "html.parser")
    return soup


def write_unique_book(book):
    """Writing datas for a single book"""
    base_path = f"Scrapping/livre seul/{book['title']}/"
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    with open(f"{base_path}{book['title']}.csv", "w") as csv_file:
        writing = csv.writer(csv_file, delimiter=";")
        writing.writerow(book.keys())
        writing.writerow(book.values())

    img_data = requests.get(book['image_url']).content
    with open(f"{base_path}{book['upc']}.jpg", 'wb') as handler:
        handler.write(img_data)


def write_unique_category(category):
    """Writing datas for a category"""
    category_name = category[0]['category']
    base_path = f"Scrapping/Categories/{category_name}/"
    images_path = f"{base_path}Images {category_name}/"
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    with open(f"{base_path}{category_name}.csv", "w") as csv_file:
        writing = csv.writer(csv_file, delimiter=";")
        writing.writerow(category[0].keys())
        for book in category:
            writing.writerow(book.values())

            img_data = requests.get(book['image_url']).content
            with open(
                    f"{images_path}{book['upc']}.jpg",
                    'wb'
                    ) as handler:
                handler.write(img_data)


def get_categories():
    """Get all the categories and their urls, returns a dict"""
    soup = get_soup()
    result = soup.find_all("li", class_="")
    categories = []
    for i in result[2:]:  # excludes 'home' and 'books'
        category = {}
        url = urllib.parse.urljoin(URL, i.a['href'])
        category['name'] = i.a.get_text().strip()
        category['index'] = url
        categories.append(category)
    return categories


def get_book(
    url=(
        "http://books.toscrape.com/catalogue/"
        "dark-notes_800/index.html"
    ),
):
    """get informations from a book"""
    book = {'product_page_url': url}
    soup = get_soup(url)
    misc = soup.find_all("td")
    book['upc'] = misc[0].renderContents().decode("utf-8")
    title = soup.find("h1").get_text().replace(";", "-")
    book['title'] = title
    book['price_including_tax'] = misc[3].string
    book['price_excluding_tax'] = misc[2].string
    availability = misc[5].renderContents().decode("utf-8")[10:-10]
    book['number_available'] = availability
    try:
        descr = soup.find(id="product_description").find_next_siblings()[0].string
    except AttributeError:
        descr = None
    book['product_description'] = descr
    category = soup.find("ul", class_="breadcrumb").findChildren()[4].get_text().strip("\n")
    book['category'] = category
    rating = soup.find("p", class_="star-rating").get_attribute_list('class')[1]
    book['review_rating'] = ratings[rating]
    img_uri = soup.find("img").get_attribute_list('src')[0]
    book['image_url'] = urllib.parse.urljoin(URL, img_uri)

    if VERBOSE:
        print(f"{book['title']}")
    return book


def get_books(
    url=(
        "http://books.toscrape.com/catalogue/"
        "category/books/fantasy_19/index.html"
    ),
    books=None,
    category="Test"
):
    """get all books from a category"""
    if books is None:
        books = []
    soup = get_soup(url)
    next = soup.find(class_="next")
    result = soup.find_all(class_="product_pod")
    for elem in result:
        page = ("/").join(elem.a['href'].split("/")[-2:])
        book_url = urllib.parse.urljoin(URL_CATALOG, page)
        book = get_book(book_url)
        books.append(book)
    if next is not None:
        next_url = urllib.parse.urljoin(url, next.a['href'])
        books = get_books(next_url, books, category)
    return books


def handle_unique_book(url):
    """Responds to CLI option --book"""
    book = get_book(url)
    write_unique_book(book)


def handle_unique_category(url):
    """Responds to CLI option --category"""
    category = get_books(url)
    write_unique_category(category)


def handle_all():
    """Responds to CLI with no option"""
    categories = get_categories()
    for category in categories:
        handle_unique_category(category['index'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--category",
        type=str, dest="category_url",
        help="Scrapp a unique category with its page url")
    parser.add_argument(
        "-b", "--book",
        type=str, dest="book_url",
        help="Scrapp a unique book with its page url")
    parser.add_argument(
        "-v", "--verbose",
        help="Display informations while scrapping (slower)",
        action="store_true")
    args = parser.parse_args()
    if args.verbose:
        global VERBOSE
        VERBOSE = True
    if args.category_url:
        handle_unique_category(args.category_url)
    elif args.book_url:
        handle_unique_book(args.book_url)
    else:
        handle_all()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n--ABORTED--")
