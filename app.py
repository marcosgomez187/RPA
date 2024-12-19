from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Usuario predeterminado
USER = "scrap"
PASSWORD = "scrap"

# Ruta para el login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USER and password == PASSWORD:
            return redirect(url_for("main"))
        else:
            return render_template("login.html", error="Credenciales incorrectas.")
    return render_template("login.html")

# Ruta para la pantalla principal
@app.route("/main")
def main():
    cards = ["Edenor", "Edesur", "Arca"]
    return render_template("index.html", cards=cards)

if __name__ == "__main__":
    app.run(debug=True)
