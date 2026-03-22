import flask
import forms
import time
from flask import Flask, render_template, request, url_for, redirect, flash
from forms import FoodForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "af60146cca6088df799eb89e625f5cb6"

lists = [
    {
        "Name": "Rice and Stew",
        "quantity": 5,
        "location": "RHIT Campus",
        "status": "Available",
        "Available_until": "17:45",
        "id": 0,
    },
    {
        "Name": "Hamburgers",
        "quantity": 5,
        "location": "Marge Food",
        "status": "Urgent",
        "Available_until": "18:00",
        "id": 1,
    },
]


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", lists=lists)


@app.route("/add", methods=["GET", "POST"])
def add_food():
    form = FoodForm()
    if form.validate_on_submit():
        new_food = {
            "Name": form.Name.data,
            "quantity": form.quantity.data,
            "location": form.location.data,
            "status": form.status.data,
            "Available_until": form.Available_until.data.strftime("%H:%M"),
            "id": len(lists),
        }
        lists.append(new_food)
        return redirect(url_for("home"))
    return render_template("food.html", form=form)


@app.route("/request/<int:id>")
def request_food(id):
    food = lists[id]
    return render_template("request.html", food=food, id=id)


@app.route("/confirm/<int:id>", methods=["POST"])
def confirm_request(id):
    lists[id]["status"] = "Reserved!"
    flash("Food Reserved Successfully!", "success")
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)