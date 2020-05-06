from flask import redirect, url_for
from flask import current_app as app


@app.route("/")
def index():
    return redirect(url_for("auth.login"))
