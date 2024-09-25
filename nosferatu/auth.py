import functools

from flask import Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        user = current_app.config["SITE_USER"]
        hashed = current_app.config["SITE_PASS"]

        if username != user:
            error = "Incorrect username."
        elif not check_password_hash(hashed, password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user"] = user
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    user = session.get("user")

    if user is None:
        g.user = None
    else:
        g.user = user


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
