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
import os
admin_email = os.getenv("ADMIN_EMAIL")
from . import order_bp

@order_bp.route("/home",methods=["GET", "POST"])
def homes():
    foods = FoodPosts.query.filter(FoodPosts.Quantity_Available > 0).all()
    return render_template("index.html", foods=foods)

@order_bp.route("/confirm_request/<int:id>", methods=["GET", "POST"])
@login_required
def request_food(id):
    form = RequestForm()
    food = FoodPosts.query.get_or_404(id)

    if not food.is_available:
        flash("This food item is not available for ordering.", "danger")
        return redirect(url_for('orders.homes'))

    if form.validate_on_submit():

        raw_quantity = form.Quantity_Ordered.data
        if raw_quantity is None:
            flash("Please enter a quantity to request.", "danger")
            return redirect(url_for('orders.request_food', id=id))

        Quantity_Ordered = int(raw_quantity)
        Quantity_Available = int(food.Quantity_Available)  # normalize stored quantity to integer


        if Quantity_Ordered > Quantity_Available:
            flash("Requested quantity exceeds available quantity!", "danger")
            return redirect(url_for('orders.request_food', id=id))
         is_valid, message = check_order_limit(current_user.id, food.restaurant_id, Quantity_Ordered)
        if not is_valid:
            flash(message, "danger")
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
        return redirect(url_for('users.UserOrders'))

    return render_template("confirm_request.html", food=food, id=id, form=form)
