from flask import Blueprint, render_template, request, redirect, url_for
from app.config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == Config.USER and password == Config.PASSWORD:
            return redirect(url_for("main.index"))
        else:
            return render_template("login.html", error="Credenciales incorrectas.")
    return render_template("login.html")