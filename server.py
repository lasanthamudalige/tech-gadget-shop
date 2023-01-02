from crypt import methods
from flask import Flask, render_template, redirect, request, session

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route("/")
def home():
    return render_template("index.html", session=session)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        return redirect("/")
    return render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmed_password = request.form.get("confirmPassword")
        print(name, email, password, confirmed_password)
        session["username"] = name
        return redirect("/")
    return render_template("sign-up.html")


@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
