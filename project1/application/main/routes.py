import requests
import json
import os

from flask import Blueprint, redirect, url_for, session, render_template, request, abort, flash
from psycopg2.extensions import AsIs
from application import db
from .forms import SearchForm, ReviewForm

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    # Only allowed logged in users
    if "username" not in session:
        flash("You have to be logged in to see this page", "danger")
        return redirect(url_for("auth.login"))

    # Show search page
    form = SearchForm()
    return render_template("main/index.html", form=form)


@bp.route("/search")
def search():
    # Only allowed logged in users
    if "username" not in session:
        flash("You have to be logged in to see this page", "danger")
        return redirect(url_for("auth.login"))

    # Generate query values
    form = SearchForm(request.args)
    query = ''.join(('%', form.query.data, '%'))
    category = form.category.data

    # Search for query in database and render
    results = db.execute("SELECT * FROM books WHERE :category ILIKE :query", {"category": AsIs(category), "query": query}).fetchall()
    return render_template("main/search.html", results=results)


@bp.route("/book/<string:isbn>")
def book(isbn):
    # Only allowed logged in users
    if "username" not in session:
        flash("You have to be logged in to see this page", "danger")
        return redirect(url_for("auth.login"))

    form = ReviewForm()
    form.isbn.data = isbn
    form.username.data = session["username"]
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()
    if book is None:
        flash("Book not found", "warning")
        return redirect(url_for("main.index"))
    reviews = db.execute("SELECT * FROM reviews WHERE isbn=:isbn", {'isbn': isbn}).fetchall()

    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("GOODREADS_KEY"), "isbns": isbn})
    average_score = goodreads.json()["books"][0]["average_rating"]
    review_count = goodreads.json()["books"][0]["work_ratings_count"]

    return render_template("main/book.html", book=book, form=form, reviews=reviews, average_score=average_score, review_count=review_count)


@bp.route("/review", methods=["POST"])
def review():
    # Only allowed logged in users
    if "username" not in session:
        flash("You have to be logged in to see this page", "danger")
        return redirect(url_for("auth.login"))

    form = ReviewForm()

    if form.validate_on_submit():
        isbn = form.isbn.data
        username = form.username.data
        rating = form.rating.data
        review = form.review.data

        if db.execute("SELECT * FROM reviews WHERE isbn=:isbn and username=:username", {'isbn': isbn, 'username': username}).fetchone() is not None:
            flash("You can only review each book once", "danger")
        else:
            db.execute("INSERT INTO reviews (isbn, username, rating, review) VALUES (:isbn, :username, :rating, :review)", {'isbn': isbn, 'username': username, 'rating': rating, 'review': review})
            db.commit()
            flash("Review submitted", "primary")
        return redirect(url_for("main.book", isbn=isbn))


@bp.route("/api/<string:isbn>")
def api(isbn):
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()
    if book is None:
        abort(404)

    goodreads = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": os.getenv("GOODREADS_KEY"), "isbns": isbn})
    average_score = goodreads.json()["books"][0]["average_rating"]
    review_count = goodreads.json()["books"][0]["work_ratings_count"]

    response = {}
    response["title"] = book["title"]
    response["author"] = book["author"]
    response["year"] = book["year"]
    response["isbn"] = isbn
    response["review_count"] = review_count
    response["average_score"] = average_score

    json.dumps(response)
    return response
