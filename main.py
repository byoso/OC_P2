#! /usr/bin/env python3
# coding: utf-8

import csv
import urllib

import requests
from bs4 import BeautifulSoup as BS

URL = "http://books.toscrape.com/"
URL_CATALOG = "http://books.toscrape.com/catalogue/"


def display_categories(categories):
    """Display categories"""
    for i,cat in enumerate(categories):
        print(f"{i+1:<3} {cat['name']:<20}: {cat['index']}")


def get_soup(url="http://books.toscrape.com/"):
    """get a soup"""
    page = requests.get(url)
    soup = BS(page.content, "html.parser")
    return soup


def csv_write(datas=None):
    headers = [
        "product_page_url",
        "upc",
        "title",
        "price_including_tax",
        "price_excluding_tax",
        "number_available",
        "product_description",
        "category",
        "review_rating",
        "image_url",
    ]
    with open("new.csv", "w") as csv_file:
        writing = csv.writer(csv_file, delimiter=",")
        writing.writerow(headers)
        if datas is not None:
            # for data in datas:
            writing.writerow(datas)


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


def get_books(
    url=(
        "http://books.toscrape.com/catalogue/"
        "category/books/fantasy_19/index.html"
        ),
    books=None,
):
    """get all books in a category"""
    if books is None:
        books = []
    soup = get_soup(url)
    next = soup.find(class_="next")
    result = soup.find_all(class_="product_pod")
    for elem in result:
        page = ("/").join(elem.a['href'].split("/")[-2:])
        books.append(urllib.parse.urljoin(URL_CATALOG, page))
    if next is not None:
        next_url = urllib.parse.urljoin(url, next.a['href'])
        books = get_books(next_url, books)
    # print(len(books))
    return books


def get_all():
    categories = get_categories()
    for cat in categories:
        cat['books'] = get_books(cat['index'])
    return categories


def main(verbose=False):
    categories = get_categories()
    if verbose:
        display_categories(categories)


if __name__ == "__main__":
    try:
        main(True)
        # get_books()
    except KeyboardInterrupt:
        print("\n--END--")
