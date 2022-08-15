#! /usr/bin/env python3
# coding: utf-8

import csv
import urllib

import requests
from bs4 import BeautifulSoup as BS

URL = "http://books.toscrape.com/"


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
    result = soup.findAll("li", class_="")
    categories = {}
    for i in result[2:]:  # excludes 'home' and 'books'
        url = urllib.parse.urljoin(URL, i.a['href'])
        categories[i.a.get_text().strip()] = url
    return categories


def get_books(url="http://books.toscrape.com/catalogue/category/books/fantasy_19/index.html"):
    """get all books in a category"""
    soup = get_soup(url)
    books = soup.find_all(class_="product_pod")
    print(books)


def main():
    categories = get_categories()
    #### debug
    for i, cat in enumerate(categories):
        print(f"{i+1:<3} {cat:<20}: {categories[cat]}")
    ####


if __name__ == "__main__":
    # main()
    get_books()
