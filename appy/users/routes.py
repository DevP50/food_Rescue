from datetime import datetime
import time
from extensions import db
from appy.models.model import login_manager, User, FoodPosts, OrderPosts
from appy.forms import RegisterForm, LoginForm, FoodForm, RequestForm
from flask import Flask, abort, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload
import os
admin_email = os.getenv("ADMIN_EMAIL")
from . import users



@users.route("/account")
def account():
    return render_template("account.html",Title='Account')

@users.route("/users/<int:id>")
@login_required
def user_profile(id):
    if current_user.id != id:
        flash("Access denied! You can only view your own profile.", "danger")
        abort(403)
    user = User.query.get_or_404(id)
    return render_template("user_profile.html", user=user,title="Profile")


@users.route("/users/my_orders/<int:id>")
@login_required
def UserOrders(id):
    if current_user.id != id:
        abort(403)
    user = User.query.get_or_404(id)#This queries the database and gets the corresponding user_id
    order = OrderPosts.query.filter_by(order_id=id).all() #this queries the order tsble and gets all the orders of a specific user
    return render_template("my_order.html",user=user,order=order,title="My Orders" )

@users.route("/logout")
@login_required
def logout():
    logout_user()#Automatically logouts out the user!
    flash("You have been logged out!", "info")
    return redirect(url_for('auth.login'))
