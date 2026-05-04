from datetime import datetime
import time
from extensions import db,login_manager
from appy.models.model import User, FoodPosts, OrderPosts
from appy.forms import RegisterForm, LoginForm, FoodForm, RequestForm

from flask import Flask, abort, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from config import admin_email
from . import order_bp

@order_bp.route("/home")
def home():
    foods = FoodPosts.query.filter(FoodPosts.Quantity_Available > 0).all()
    return render_template("index.html", foods=foods)

@order_bp.route("/confirm_request/<int:id>", methods=["GET", "POST"])
@login_required
def request_food(id):
    form = RequestForm()
    food = FoodPosts.query.get_or_404(id)

    if not food.is_available:
        flash("This food item is not available for ordering.", "danger")
        return redirect(url_for('orders.home'))

    if form.validate_on_submit():

        Quantity_Ordered = form.Quantity_Ordered.data
        Quantity_Available = food.Quantity_Available #We need to convert the quantity available to an integer because it is stored as a string in the database and we need to compare it with the quantity ordered which is an integer    

        if Quantity_Ordered is None: #If there is no value for Quantity ordered
            flash("Please enter a quantity to request.", "danger")
            return redirect(url_for('orders.request_food', id=id))
 

        if Quantity_Ordered > Quantity_Available:
            flash("Requested quantity exceeds available quantity!", "danger")
            return redirect(url_for('orders.request_food', id=id))

        today = datetime.utcnow().date()
        user_orders_today = OrderPosts.query.options(joinedload(OrderPosts.food)).filter(
            OrderPosts.order_id == current_user.id,
            func.date(OrderPosts.created_at) == today
        ).all()

        total_portions_today = sum(o.quantity_ordered for o in user_orders_today)
        restaurants_today = {o.food.restaurant_id for o in user_orders_today if o.food}
        if total_portions_today + Quantity_Ordered > 3:
            flash("You can only request up to 3 portions per day.", "danger")
            return redirect(url_for('orders.request_food', id=id))

        if food.restaurant_id not in restaurants_today and len(restaurants_today) >= 2:
            flash("You can only order from a maximum of 2 different restaurants per day.", "danger")
            return redirect(url_for('orders.request_food', id=id))

        new_order = OrderPosts(
            order_id=current_user.id,
            food_id=food.id,
            quantity_ordered=Quantity_Ordered,
            total_price=Quantity_Ordered * food.price,
        )

        food.Quantity_Available = Quantity_Available - Quantity_Ordered
        if food.Quantity_Available <= 0:
            food.status = "Sold Out"

        db.session.add(new_order)
        db.session.add(food)
        db.session.commit()

        flash("Request submitted successfully!", "success")
        return redirect(url_for('orders.home'))

    return render_template("confirm_request.html", food=food, id=id, form=form)