from flask import Blueprint, render_template, request, redirect, url_for, session
from app.config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == Config.USER and password == Config.PASSWORD:
            # Almacenar el nombre de usuario en la sesión
            session['username'] = username
            return redirect(url_for("main.index"))
        else:
            return render_template("login.html", error="Credenciales incorrectas.")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    # Eliminar el nombre de usuario de la sesión
    session.pop('username', None)
    return redirect(url_for("auth.login"))
