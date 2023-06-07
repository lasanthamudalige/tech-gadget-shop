from flask import Flask, render_template, redirect, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from email_validator import validate_email, EmailNotValidError
import sqlalchemy


# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bookshop.db"
# This is to ignore deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# initialize the app with the extension
db.init_app(app)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(250))


# Run once to create a db
# with app.app_context():  # From SQLAlchemy 3.0
#     db.create_all()

app.secret_key = b'90dca4e5e781de815882c46061ec3813f7eafb3eb63c8000316f99dda92c262d'


@app.route("/")
def home():
    return render_template("index.html", session=session)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            validation = validate_email(email)
            
            try:
                user = db.session.execute(db.select(Users).filter_by(email=email)).one()

                if user[0].password != password:
                    flash("Invalid password.", category="error")
                else:
                    session["username"] = user[0].name
                    return redirect("/")
            
            except sqlalchemy.exc.NoResultFound as e:
                flash("User not found.", category="error")

        except EmailNotValidError as e:
            flash("Invalid email address.", category="error")
    return render_template("login.html")


@ app.route("/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmed_password = request.form.get("confirmPassword")
        if password == confirmed_password:
            print(name, email, password, confirmed_password)
            new_user = Users(name= name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
        else: 
            pass
            # session["username"] = name
        return redirect("/")
    return render_template("sign-up.html")


@ app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
