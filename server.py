import datetime
from functools import wraps
from flask import Flask, render_template, redirect, request, session, flash, abort
from flask_sqlalchemy import SQLAlchemy
from email_validator import validate_email, EmailNotValidError


# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///techshop.db"
# This is to ignore deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# create the extension
db = SQLAlchemy(app)
# initialize the app with the extension
db.init_app(app)


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class FeaturedProducts(db.Model):
    __tablename__ = "featured_products"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(250))


class PopularProducts(db.Model):
    __tablename__ = "popular_products"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(250))


# Run once to create a db
# with app.app_context():  # From SQLAlchemy 3.0
#     db.create_all()

app.secret_key = b'90dca4e5e781de815882c46061ec3813f7eafb3eb63c8000316f99dda92c262d'

today = datetime.date.today()
year = today.year

def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session["id"] != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function

@app.route("/")
def home():
    return render_template("index.html", session=session, year=year)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            validation = validate_email(email)
            
            user = Users.query.filter_by(email=email).first()

            if user == None:
                flash("User not found.", category="error")
            elif user.password != password:
                flash("Invalid password.", category="error")
            else:
                session["id"] = user.id
                print(user.id)
                session["username"] = user.name
                session["email"] = user.email

                return redirect("/")          

        except EmailNotValidError as e:
            flash("Invalid email address.", category="error")

    return render_template("login.html", login_page=True, year=year)


@app.route("/signup", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmed_password = request.form.get("confirmPassword")

        try:
            validation = validate_email(email)

            if password == confirmed_password:

                user = Users.query.filter_by(email=email).first()

                if user == None:
                    new_user = Users(name= name, email=email, password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    session["id"] = new_user.id
                    session["username"] = name
                    session["email"] = email
                    return redirect("/")
                else:
                    flash("Account already exist.", category="error")                     
                
            else: 
                flash("Passwords do not match.", category="error")

        except EmailNotValidError as e:
            flash("Invalid email address.", category="error")
 
    return render_template("sign-up.html", login_page=True, year=year)


@app.route("/logout")
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session.pop('email', None)
    return redirect("/")


@app.route("/admin")
@admin_only
def admin():
    return render_template("admin.html", login_page=True, year=year)

if __name__ == "__main__":
    app.run(debug=True)
