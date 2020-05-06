from flask import Blueprint, render_template, redirect, url_for, session, flash
from werkzeug import generate_password_hash, check_password_hash

from application import db
from .forms import RegistrationForm, LoginForm

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if "username" in session:
        flash("You are already logged in", "secondary")
        return redirect(url_for("main.index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Get data from form
        username = form.username.data
        password = generate_password_hash(form.password.data, method="SHA256")

        # If username already exists, reject
        if db.execute("SELECT * FROM users WHERE username=:username", {"username": username}).first() is not None:
            flash("User already exists", "warning")
            return redirect(url_for("auth.register"))

        # Register user
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)", {
                   "username": username, "password": password})
        db.commit()

        session["username"] = username
        flash("Registration successful", "success")
        return redirect(url_for("main.index"))
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if "username" in session:
        flash("You are already logged in", "secondary")
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        # Get data from form
        username = form.username.data
        password = form.password.data

        # If username does not exists, reject
        user = db.execute(
            "SELECT * FROM users WHERE username=:username", {"username": username}).first()
        if user is None:
            flash("User does not exist", "warning")
            return redirect(url_for("auth.login"))

        # If wrong password, reject
        if not check_password_hash(user["password"], password):
            flash("Wrong password", "warning")
            return redirect(url_for("auth.login"))

        session["username"] = user["username"]
        flash("Login successful", "success")
        return redirect(url_for("main.index"))
    return render_template("auth/login.html", form=form)


@bp.route("/logout", methods=["GET", "POST"])
def logout():
    if "username" not in session:
        flash("You are not logged in", "warning")
        return redirect(url_for("auth.login"))

    session.pop("username", None)
    flash("Logout successful", "secondary")
    return redirect(url_for("main.index"))
