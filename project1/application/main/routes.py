from flask import Blueprint, redirect, url_for, session, render_template, request
from psycopg2.extensions import AsIs
from application import db
from .forms import SearchForm, ReviewForm

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    form = SearchForm()
    return render_template("main/index.html", form=form)


@bp.route("/search")
def search():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    form = SearchForm(request.args)
    query = ''.join(('%', form.query.data, '%'))
    category = form.category.data

    results = db.execute("SELECT * FROM books WHERE :category ILIKE :query", {"category": AsIs(category), "query": query}).fetchall()
    return render_template("main/search.html", results=results)


@bp.route("/book/<string:isbn>")
def book(isbn):
    if "username" not in session:
        return redirect(url_for("auth.login"))

    form = ReviewForm()
    form.isbn.data = isbn
    form.username.data = session["username"]
    book = db.execute("SELECT * FROM books WHERE isbn=:isbn", {'isbn': isbn}).fetchone()
    reviews = db.execute("SELECT * FROM reviews WHERE isbn=:isbn", {'isbn': isbn}).fetchall()

    return render_template("main/book.html", book=book, form=form, reviews=reviews)


@bp.route('/review', methods=['POST'])
def review():
    if "username" not in session:
        return redirect(url_for("auth.login"))

    form = ReviewForm()

    if form.validate_on_submit():
        isbn = form.isbn.data
        username = form.username.data
        rating = form.rating.data
        review = form.review.data

        if db.execute("SELECT * FROM reviews WHERE isbn=:isbn and username=:username", {'isbn': isbn, 'username': username}).fetchone() is not None:
            return "You can only review each book once"
        db.execute("INSERT INTO reviews (isbn, username, rating, review) VALUES (:isbn, :username, :rating, :review)", {'isbn': isbn, 'username': username, 'rating': rating, 'review': review})
        db.commit()
        return redirect(url_for("main.book", isbn=isbn))
