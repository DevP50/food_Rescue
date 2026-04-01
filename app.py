from forms import RegistrationForm, LoginForm, FoodForm, RequestForm
import flask
import time
from flask import Flask, render_template, request, url_for, redirect, flash


app = Flask(__name__)
app.config["SECRET_KEY"] = "af60146cca6088df799eb89e625f5cb6"

lists = [
    {
        "Name": "Rice and Stew",
        "Quantity_Available": 5,
        "location": "RHIT Campus",
        "status": "Available",
        "Available_until": "17:45",
        "lat": 35.9132,
        "lng": -79.0558,
        "id": 0
    }
    ,
    {
        "Name": "Hamburgers",
        "quantity": 5,
        "location": "Marge Food",
        "status": "Urgent",
        "Available_until": "18:00",
        "lat": 35.9132,
        "lng": -79.0558,
        "id": 1
    },
]
users = []



@app.route("/")
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = {
            "username": form.username.data,
            "email": form.email.data,
            "password": form.password.data,
            "role": form.Role.data
        }
        if form.Role.data  == "Restaurant":
            new_user["restaurant_name"] = form.restaurant_name.data
            new_user["Location"] = form.Location.data
            new_user["phone"] = form.phone.data

        users.append(new_user)
        
        flash("Registration successful!", "success")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)

@app.route("/home")
def home():
    return render_template("index.html", lists=lists)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "nanagilbertjunior3@gmail.com" and form.password.data == "password":
            flash("You have been logged in!","success")
            return redirect(url_for('home'))
        else:
            flash("Password Email incorrect! Try Again","error")
                            
    return render_template('login.html',form=form)

    

@app.route("/home")
def home_page():
    return render_template("index.html", lists=lists)


@app.route("/add", methods=["GET", "POST"])
def add_food():
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
            "quantity": form.quantity.data,
            "longitude": form.longitude.data,
            "latitude": form.latitude.data,
            "location_name": form.location_name.data or "Unknown",  # Add location field
            "status": form.status.data,
            "Available_until": form.Available_until.data.strftime("%H:%M"),
            "id": len(lists)
        }

        lists.append(new_food)
        return redirect(url_for("home"))

    return render_template("food.html", form=form)


@app.route("/confirm_request/<int:id>")
def request_food(id):
    form =RequestForm()
    food = lists[id]
    return render_template("confirm_request.html", food=food, id=id,form=form)


@app.route("/confirm/<int:id>", methods=["POST"])
def confirm_request(id):
    lists[id]["status"] = "Reserved!"
    form=FoodForm()
    Quantity_left = lists[id]["Quantity_Available"] - int(request.form.get("Quantity_Ordered"))
    lists[id]["Quantity_Available"] = Quantity_left
    flash("Food Reserved Successfully!", "success")
    return redirect(url_for("home"))

from flask import request

@app.route('/set_location', methods=['POST'])
def set_location():
    data = request.get_json()
    lists['lat'] = data['lat']
    lists['lng'] = data['lng']
    return '', 204

import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.route('/nearby_food')
def nearby_food():
    user_lat = request.form.get('lat')
    user_lng = request.form.get('lng')

    foods = [food for food in lists if lists['status'] == 'Available'] 
    nearby = []

    for food in lists:
        distance = calculate_distance(
            user_lat, user_lng,
            food.lat, food.lng
        )
        
        if distance < 10:  # within 10 km
            food.distance = round(distance, 2)
            nearby.append(food)

    # sort by nearest
    nearby.sort(key=lambda f: f.distance)
   
    return render_template('nearby.html', lists=nearby)


if __name__ == "__main__":
    app.run(debug=True)