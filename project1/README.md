# Project 1: Books

Books is a Flask application to search for books in a given database. Additionally, it shows ratings from Goodreads.

Users are required to register for an account and log in before using the search function.

Users can search for books via either the title, ISBN number or author. On each individual book page, users are able to see reviews left by others and leave their own review. Each user is only allowed one review per book.

## Requirements

The following environment variables need to be set:

`FLASK_APP=application` – application entry point

`DATABASE_URL` – URL for SQL database (use Postgres for compatibility)

`SECRET_KEY` – Secret key for app

`GOODREADS_KEY` – API key for Goodreads

## Usage

Install dependencies:

```bash
pip3 install -r requirements.txt
```

Import csv into database:

```bash
python3 import.py
```

Run application:

```bash
flask run
```

## API

API access is given by accessing the `/api/<isbn>` route, where `<isbn>` is the isbn number of the book to be accessed. The resulting JSON will be in this format:

```JSON
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}
```