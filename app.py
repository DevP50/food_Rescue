from datetime import datetime
import time
from flask import Flask, render_template, request, url_for, redirect, flash
from models import db, login_manager, User, FoodPosts, OrderPosts
from forms import RegisterForm, LoginForm, FoodForm, RequestForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["SECRET_KEY"] = "af60146cca6088df799eb89e625f5cb6"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
#Every class is a table in the database, and every object of the class is a column in the table.
lists=  [ 
      {
          "image": "burger.jpg",
        "Name": "TCHOP ET YAMO",
        "Quantity_Available": 5,
        "longitude": "4.6",
        "latitude": "4.04",
        "location_name": "Bonamoussadi",  # Add location field
        "status": "available",
        "Available_until": "18:00",
        "food_name": "Egusi Soup",
        "id" : 0
         },
         {
            "Name": "TCHOP ET YAMO",
            "Quantity_Available": 5,
            "longitude": "4.6",
            "latitude": "4.04",
            "location_name": "Bonamoussadi",  # Add location field
             "status": "available",
             "Available_until": "18:00",
            "food_name": "Beignet et Haricot",
            "id" : 1
         }
]


@app.route("/")
@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Hash the password before storing
        hashed_password = check_password_hash(user.password,form.password.data)
        
        # Check if the role is Restaurant and validate required fields
        if form.Role.data == "Restaurant":
            if not form.restaurant_name.data:
                flash("Restaurant name is required for restaurants!", "danger")
                return render_template("register.html", form=form)
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                role=form.Role.data,
                phone=form.phone.data,
                restaurant_name=form.restaurant_name.data,
                restaurant_location=form.restaurant_location.data
            )
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashed_password,
                role=form.Role.data,
                phone=form.phone.data
            )
    
        try:
            db.session.add(user)    
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed: {str(e)}", "danger")
            return render_template("register.html", form=form)
    
    return render_template("register.html", form=form)

@app.route("/home")
def home():

    return render_template("index.html",lists=lists)   

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check if user exists and password matches
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
    else:
            flash("Email or Password incorrect! Try Again", "danger")
                            
    return render_template('login.html',form=form)



@app.route("/account")
def account():
    return render_template("account.html",Title='Account')


    

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_food():
    if current_user.role != "Restaurant":
        flash("Only restaurants can add food!", "danger")
        return redirect(url_for('home'))
    
    form = FoodForm()

    if form.validate_on_submit():
        image_file = form.image.data
        image_filename = None
        if image_file:
            image_filename = image_file.filename
            image_file.save(f"static/{image_filename}")

        new_food = {
            "image": image_filename,
            "Name": form.Name.data,
            "Quantity_Available": form.Quantity_Available.data,
            "longitude": form.longitude.data,
            "latitude": form.latitude.data,
            "location_name": form.location_name.data or "Unknown",
            "status": form.status.data,
            "Available_until": form.Available_until.data.strftime("%H:%M"),
            "id": len(lists),
            "restaurant_id": current_user.id
        }

        lists.append(new_food)
        flash("Food added successfully!", "success")
        return redirect(url_for("restaurant"))

@app.route("/confirm_request/<int:id>", methods=["GET", "POST"])
def request_food(id):
    form = RequestForm()
    food = lists[id]

    if form.validate_on_submit():#If the form is valid then execute the form below
        Quantity_Ordered = form.Quantity_Ordered.data
        Quantity_Available = food.get("Quantity_Available", 0)
     
        if Quantity_Ordered is None:
            flash("Please enter a quantity to request.", "danger")
            return redirect(url_for('request_food', id=id))

        if Quantity_Ordered > Quantity_Available:
            flash("Requested quantity exceeds available quantity!", "danger")
            return redirect(url_for('home'))
              
        food["Quantity_Available"] = Quantity_Available - Quantity_Ordered
        flash("Request submitted successfully!", "success")
        return redirect(url_for('home'))
 
    return render_template("confirm_request.html", food=food, id=id, form=form, lists=lists)


@app.route("/restaurant")
@login_required
def restaurant():
    if current_user.role != "Restaurant":
        flash("Access denied! Only restaurants can view this page.", "danger")
        return redirect(url_for('home'))
    
    # Get foods added by this restaurant (for now, all foods since no owner field)
    restaurant_foods = [food for food in lists if food.get("restaurant_id") == current_user.id]
    
    return render_template("restaurant.html", foods=restaurant_foods)

@app.route("/restaurant/delete/<int:id>", methods=["POST"])
@login_required
def delete_food(id):
    if current_user.role != "Restaurant":
        flash("Access denied!", "danger")
        return redirect(url_for('home'))
    
    # Find and remove the food if it belongs to this restaurant
    for food in lists:
        if food.get("id") == id and food.get("restaurant_id") == current_user.id:
            lists.remove(food)
            flash("Food deleted successfully!", "success")
            break
    else:
        flash("Food not found or access denied.", "danger")
    
    return redirect(url_for('restaurant'))

@app.route("/restaurant/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_food(id):
    if current_user.role != "Restaurant":
        flash("Access denied!", "danger")
        return redirect(url_for('home'))
    
    # Find the food
    food = None
    for f in lists:
        if f.get("id") == id and f.get("restaurant_id") == current_user.id:
            food = f
            break
    
    if not food:
        flash("Food not found or access denied.", "danger")
        return redirect(url_for('restaurant'))
    
    form = FoodForm()
    
    if request.method == "GET":
        # Pre-populate form with current values
        form.Name.data = food.get("Name")
        form.Quantity_Available.data = food.get("Quantity_Available")
        form.status.data = food.get("status")
        # Note: Other fields like time, location would need more complex handling
    
    if form.validate_on_submit():
        food["Name"] = form.Name.data
        food["Quantity_Available"] = form.Quantity_Available.data
        food["status"] = form.status.data
        # Update other fields as needed
        flash("Food updated successfully!", "success")
        return redirect(url_for('restaurant'))
    
    return render_template("update_food.html", form=form, food=food)
   

@app.route('/set_location', methods=['POST'])
def set_location():
    data = request.get_json()
    lists['lat'] = data['lat']
    lists['lng'] = data['lng']
    return '', 204

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", "info")
    return redirect(url_for('login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)