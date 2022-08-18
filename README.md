# Books to scrape

## How to run this program

### Virtual environment

To run this program you will need to install some dependencies. The best way to do so is to create a virtual environment first.

Open a terminal in the root directory of this project, then type:
```
$ python3 -m venv env
```

and then activate this virtual environment:

```
$ source env/bin/activate
```

once you'll be done withe this program, simply deactivate the virtual environment this way:

```
$ deactivate
```

### Install the dependecies

With the virtual environment activated, do:
```
$ pip install -r requirements.txt
```


### Launch the program

You can see the different options of the program with:
```
$ ./main.py -h
```

Scrap only one book like this (with the book's url of your choice):
```
$ ./main.py --book http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html
```

Scrap only one category of books (with the url of the category's page of your choice):
```
$ ./main.py --category http://books.toscrape.com/catalogue/category/books/science-fiction_16/index.html
```

Scrap all the books from Books to Scrape:
```
$ ./main.py
```
