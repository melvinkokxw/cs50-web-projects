import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

db.execute("CREATE SCHEMA IF NOT EXISTS public")
db.execute("DROP TABLE IF EXISTS books CASCADE")
db.execute("CREATE TABLE IF NOT EXISTS books (isbn varchar(60) PRIMARY KEY, title varchar(120) NOT NULL, author varchar(120) NOT NULL, year int NOT NULL)")

with open("books.csv") as csvfile:
    books = csv.DictReader(csvfile)
    for book in books:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {
                   "isbn": book["isbn"], "title": book["title"], "author": book["author"], "year": book["year"]})
    db.commit()
