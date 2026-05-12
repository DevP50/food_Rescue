from datetime import datetime
import time

from extensions import db,login_manager
from appy.models.model import User, FoodPosts, OrderPosts
from appy.forms import RegisterForm, LoginForm, FoodForm, RequestForm
from flask import Flask, abort, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload
import os
admin_email = os.getenv("ADMIN_EMAIL")
from . import admin_bp
def admin_required():
    if not current_user.is_authenticated or current_user.email != admin_email:
        flash("Access denied! You are not an admin.", "danger")
        abort(403)

@admin_bp.route('/admin')
@login_required
def admin_():
    admin_required()

    users = User.query.filter(User.role == 'User').all()#Get all the users in the User model with role User
    restaurants = User.query.filter(User.role == 'Restaurant').all()
    riders = User.query.filter(User.role == 'Food Delivery').all()
    food_posts = FoodPosts.query.options(joinedload(FoodPosts.restaurant)).all()
    orders = OrderPosts.query.options(joinedload(OrderPosts.order), joinedload(OrderPosts.food)).all()


    return render_template(
        'admin.html',
        title="Admin Dashboard",
        users=users,
        restaurants=restaurants,
        riders=riders,
        food_posts=food_posts,
        orders=orders
    )

@admin_bp.route('/admin/user/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_user(id):
    admin_required()

    user = User.query.get_or_404(id)
    if user.email == admin_email:
        flash('Cannot delete the admin account.', 'warning')
        return redirect(url_for('admin.admin_'))
          
    # Remove child records first to avoid orphaned references
    if user.role == 'Restaurant':
        food_ids = [food.id for food in FoodPosts.query.filter_by(restaurant_id=user.id).all()]
        if food_ids:
            OrderPosts.query.filter(OrderPosts.food_id.in_(food_ids)).delete(synchronize_session=False)
        FoodPosts.query.filter_by(restaurant_id=user.id).delete(synchronize_session=False)

        OrderPosts.query.filter_by(order_id=user.id).delete(synchronize_session=False)
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
        return redirect(url_for('admin.admin_'))
    return render_template(
        "admin.html",
        title="Users Management",
        users="users",
     )

@admin_bp.route('/admin/post/delete/<int:id>', methods=['POST'])
@login_required
def admin_delete_post(id):
    admin_required()
    food = FoodPosts.query.get(id)
    if food:
     OrderPosts.query.filter_by(food_id=food.id).delete(synchronize_session=False)
     db.session.delete(food)
     db.session.commit()
     flash('Restaurant post deleted successfully.', 'success')
     return redirect(url_for('aadmin_'))
    return render_template("admin.html")

@admin_bp.route('/admin/order/update/<int:id>', methods=['POST'])
@login_required
def admin_update_order(id):
    admin_required()

    order = OrderPosts.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status in ['Pending', 'Accepted', 'Delivered', 'Rejected', 'Paid']:
        order.order_status = new_status
        if new_status == 'Accepted':
            order.accepted_at = datetime.utcnow()
        if new_status == 'Delivered':
            order.delivered_at = datetime.utcnow()
        db.session.commit()
        flash('Order status updated successfully.', 'success')
    else:
        flash('Invalid order status.', 'danger')

    return redirect(url_for('admin_'))

@admin_bp.route('/admin/rider/add', methods=['POST'])
@login_required
def admin_add_rider():
    admin_required()

    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    phone = request.form.get('phone', '').strip()

    if not username or not email:
        flash('Rider name and email are required.', 'danger')
        return redirect(url_for('admin_'))

    if User.query.filter_by(email=email).first():
        flash('A user with that email already exists.', 'danger')
        return redirect(url_for('admin_'))

    rider = User(username=username, email=email, password='placeholder', role='Food Delivery', phone=phone)
    db.session.add(rider)
    db.session.commit()
    flash('Rider account added successfully.', 'success')
    return redirect(url_for('admin_'))
