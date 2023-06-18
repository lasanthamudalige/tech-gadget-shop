from flask import Flask, render_template, redirect, request, session, flash, abort
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from functools import wraps
import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from email_validator import validate_email, EmailNotValidError
import stripe
import os
from dotenv import load_dotenv

load_dotenv()
# This is your test secret API key.
stripe.api_key = os.environ.get("STRIPE_APIT_KEY")


# create the app
app = Flask(__name__)
# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///techshop.db"
# initialize the app with the extension
db.init_app(app)


# Flask login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float, nullable=False)
    img_url = db.Column(db.String(250))



def add_default_data():
    if not Item.query.filter_by(name="Smart Speaker Pro").first():
        item1 = Item(
            name="Smart Speaker Pro", 
            category="featured",
            description="Experience the future of home entertainment with our voice-controlled smart speakers, combining convenience, immersive sound, and seamless control over music, podcasts, and smart home devices, revolutionizing your home interaction.", 
            price=199.99, 
            img_url="https://images.pexels.com/photos/14309805/pexels-photo-14309805.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            )
        db.session.add(item1)

    if not Item.query.filter_by(name="InfinityEdge Smartphone").first():
        item2 = Item(
            name="InfinityEdge Smartphone",
            category="popular",
            description="Explore limitless possibilities with edge-to-edge displays and powerful performance.", 
            price=899.99, 
            img_url="https://images.pexels.com/photos/207455/pexels-photo-207455.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            )
        db.session.add(item2)
    
    if not Item.query.filter_by(name="Gaming Laptop Elite").first():   
        item3 = Item(
            name="Gaming Laptop Elite", 
            category="popular",
            description="Elevate your gaming experience with seamless gameplay and immersive graphics.", 
            price=1499.99, 
            img_url="https://images.pexels.com/photos/12300693/pexels-photo-12300693.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            )
        db.session.add(item3)
        
    if not Item.query.filter_by(name="Wireless Noise-Canceling Headphone").first():
        item4 = Item(
            name="Wireless Noise-Canceling Headphone", 
            category="popular",
            description="Immerse yourself in pristine sound with cutting-edge technology and superior comfort.", 
            price=249.99, 
            img_url="https://images.pexels.com/photos/7241360/pexels-photo-7241360.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            )
        db.session.add(item4)
    
    if not Item.query.filter_by(name="Fitness Smartwatch Plus").first():
        item5 = Item(
            name="Fitness Smartwatch Plus", 
            category="popular",
            description="Stay active and track your fitness goals with a sleek smartwatch that keeps you connected and motivated.", 
            price=129.99, 
            img_url="https://images.pexels.com/photos/437037/pexels-photo-437037.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            )
        db.session.add(item5) 
    
    if not Item.query.filter_by(name="Ultra-Slim Tablet Pro").first():
        item6 = Item(
            name="Ultra-Slim Tablet Pro", 
            category="popular",
            description="Experience style and functionality on the go with a portable tablet that offers a stunning display and powerful performance.", 
            price=399.99, 
            img_url="https://images.pexels.com/photos/6373018/pexels-photo-6373018.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
            )
        db.session.add(item6)

    db.session.commit()


# Run once to create a db
# with app.app_context():  # From SQLAlchemy 3.0
#     db.create_all()
#     add_default_data()

 
app.secret_key = b'90dca4e5e781de815882c46061ec3813f7eafb3eb63c8000316f99dda92c262d'


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    items = Item.query.all()

    cart = None
    total_items = 0 

    if "cart" in session:
      cart = session["cart"]
      for item in cart:
        total_items += item["quantity"]
      
    return render_template("index.html", 
                           year=datetime.date.today().year, 
                           current_user=current_user,
                           items=items,
                           total_items=total_items,
                           cart=cart)


@app.route("/login", methods=["Get","POST"])
def login():

    cart = None
    total_items = 0  

    if session["cart"]:
      cart = session["cart"]
      for item in cart:
        total_items += item["quantity"]

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        try:
            validation = validate_email(email)
            
            user = User.query.filter_by(email=email).first()

            if user == None:
                flash("User not found.", category="error")
            elif not check_password_hash(user.password, password):
                flash("Invalid password.", category="error")
            else:
                login_user(user)

                return redirect("/")          

        except EmailNotValidError as e:
            flash("Invalid email address.", category="error")

    return render_template("login.html", less_content=True, year=datetime.date.today().year, current_user=current_user, total_items=total_items, cart=cart)


@app.route("/signup", methods=["Get", "POST"])
def sign_up():

    cart = None
    total_items = 0  

    if session["cart"]:
      cart = session["cart"]
      for item in cart:
        total_items += item["quantity"]

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmed_password = request.form.get("confirmPassword")

        try:
            validate_email(email)

            if password == confirmed_password:

                user = User.query.filter_by(email=email).first()

                if user == None:
                    salted_hashed_password = generate_password_hash(password=password, salt_length=16)
                    new_user = User(name=name, email=email, password=salted_hashed_password)
                    db.session.add(new_user)
                    db.session.commit()

                    login_user(new_user)
                    session.pop('_flashes', None)
                    return redirect("/")
                else:
                    flash("Account already exist.", category="error")                     
                
            else: 
                flash("Passwords do not match.", category="error")

        except EmailNotValidError as e:
            flash("Invalid email address.", category="error")
 
    return render_template("sign-up.html", less_content=True, year=datetime.date.today().year, current_user=current_user, total_items=total_items, cart=cart)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/admin")
@login_required
@admin_only
def admin():
    items = Item.query.all()


    return render_template("admin.html", year=datetime.date.today().year, current_user=current_user,items=items, admin=True)


@app.route("/add_item", methods=["Get", "POST"])
@login_required
@admin_only
def add_item():
    if request.method == "POST":
        item_type = request.form.get("product-type")
        item_name = request.form.get("item-name")
        item_image_url = request.form.get("item-image")
        item_price = float(request.form.get("item-price"))
        item_description = request.form.get("item-description")
        print(item_type)
        
        if item_type == "" or item_name == "" or item_image_url == "" or item_price == "" or item_description == "":
            flash("Please fill all the input fields.", "error")
        else:
            if item_type == "Featured Product":
                new_item = Item(name=item_name, category="featured" , img_url=item_image_url, price=item_price, description=item_description)

            elif item_type == "Popular Product":
                new_item = Item(name=item_name, category="popular" , img_url=item_image_url, price=item_price, description=item_description)

            db.session.add(new_item)
            db.session.commit()

            session.pop('_flashes', None)
            return redirect("/admin")

    # If request method is 'GET'
    return render_template("add.html", login_page=True, year=datetime.date.today().year, current_user=current_user, less_content=True)


@app.route("/edit/<item_id>", methods=["Get", "POST"])
@login_required
@admin_only
def edit_item(item_id):
    if request.method == "POST":
        item_type = request.form.get("product-type")
        item_name = request.form.get("item-name")
        item_image_url = request.form.get("item-image")
        item_price = float(request.form.get("item-price"))
        item_description = request.form.get("item-description")

        if item_type == "" or item_name == "" or item_image_url == "" or item_price == "" or item_description == "":
            flash("Please fill all the input fields.", "error")
        else:
            found_item = Item.query.filter_by(id=item_id).first()
                
            found_item.name = item_name
            found_item.img_url = item_image_url
            found_item.price = item_price
            found_item.description = item_description
            db.session.commit()
                
            flash("Item successfully update.", "message")

            session.pop('_flashes', None)
            return redirect("/admin")
    
    # For 'GET' requests
    found_item = Item.query.filter_by(id=item_id).first()
    return render_template("edit.html", less_content=True, year=datetime.date.today().year, current_user=current_user, admin=True, item=found_item)

    
@app.route("/delete/<item_id>", methods=["Get", "POST"])
@login_required
@admin_only
def delete_item(item_id):
    found_item = Item.query.filter_by(id=item_id).first()
    
    if found_item:         
        db.session.delete(found_item)
        db.session.commit()

                    
    return redirect("/admin")


@app.route("/add-to-cart/<item_id>/<checkout>")
def add_to_cart(item_id, checkout):
    product = Item.query.filter_by(id=item_id).first()

    if product:
        if "cart" in session:
            cart = session["cart"] 
            found = False
            for item in session["cart"]:
                if item["name"] == product.name:
                    found = True
                    new_quantity = item["quantity"] + 1
                    item.update({"quantity" : new_quantity})
            
            if not found:
                cart.append({"id": product.id, "name": product.name, "image": product.img_url , "price": product.price, "quantity": 1})
            session["cart"] = cart
        
        else: 
            session["cart"] = []
            session["cart"].append({"id": product.id, "name": product.name, "image": product.img_url , "price": product.price, "quantity": 1})
        
        print(session["cart"])
    print(checkout)

    if checkout == "True":
        return redirect("/checkout")
    else:
        return redirect("/")


@app.route("/remove-from-cart/<item_id>")
def remove_from_cart(item_id):
    product = Item.query.filter_by(id=item_id).first()

    if product:
        if "cart" in session:
            cart = session["cart"] 
            for item in session["cart"]:
                if item["name"] == product.name:
                    quantity = item["quantity"]
                    if quantity == 1:
                        cart.remove(item)
                    else: 
                        new_quantity = item["quantity"] - 1
                        item.update({"quantity" : new_quantity})

                session["cart"] = cart
        
    return redirect("/checkout")    



@app.route("/checkout")
def checkout():
    
    cart = None
    total_items = 0 
    total_amount = 0 
    if "cart" in session:
      cart = session["cart"]
      for item in cart:
        total_items += item["quantity"]
        total_amount += item["quantity"] * item["price"]

    return render_template("checkout.html", year=datetime.date.today().year ,less_content=True ,total_items=total_items, cart=cart, total_amount=round(total_amount, 2), date=datetime.date.today())


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    try:
        line_items = []
        for item in session["cart"]:
            line_item = {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": item["name"], 
                                     "images": [item["image"]]
                                     },
                    "unit_amount_decimal": item["price"] * 100,
                    # "custom_unit_amount": 1,
                },
                "quantity": item["quantity"],
            }
            line_items.append(line_item)

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode='payment',
            billing_address_collection= "required",
            success_url="http://127.0.0.1:5000/success",
            cancel_url= "http://127.0.0.1:5000/"
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


@app.route("/success")
def success():
    # Update cart to None to remove everything in it
    cart = session["cart"]
    cart = None
    # Assign cart to None
    session["cart"] = cart
    total_items = 0  
    
    return render_template("success.html", less_content=True, cart=cart, total_items=total_items)

if __name__ == "__main__":
    app.run(port=5000 ,debug=True)
