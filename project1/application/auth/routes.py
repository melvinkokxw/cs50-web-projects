from flask import Blueprint, render_template, redirect, url_for, session

from application import db
from .forms import RegistrationForm, LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Get data from form
        username = form.username.data
        password = form.password.data

        # If username already exists, reject
        if db.execute("SELECT * FROM users WHERE username=:username", {"username": username}).first() is not None:
            return "user already exists"

        # Register user
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {
                   "username": username, "password": password})
        db.commit()
        return "user registered"
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Get data from form
        username = form.username.data
        password = form.password.data

        # If username does not exists, reject
        user = db.execute(
            "SELECT * FROM users WHERE username=:username", {"username": username}).first()
        if user is None:
            return "user does not exists"

        # If wrong password, reject
        if password != user["password"]:
            return "wrong password"

        session["username"] = user["username"]
        return "logged in"
    return render_template("auth/login.html", form=form)


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return redirect(url_for("auth.login"))
