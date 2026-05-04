
from datetime import datetime
from extensions import db, login_manager
from appy.models.model import FoodPosts, OrderPosts
from appy.forms import FoodForm,RegisterForm
from flask import abort, render_template, request, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload
from . import restauraunt_bp
@restauraunt_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_food():
    if current_user.role != "Restaurant":
        flash("Only restaurants can add food!", "danger")
        return redirect(url_for('home'))
    
    print("Route HI")
    
    form = FoodForm()
    
    
    if form.validate_on_submit():
        print("FORM SUBMITTED")
        if request.method == "POST":
         print("REQUEST POST")
         image_file = form.image.data
         image_filename = None
         if image_file:
            image_filename = image_file.filename
            image_file.save(f"static/{image_filename}")
         from datetime import datetime

         

         name = form.Name.data
         status = form.status.data
         location_name = form.location_name.data or "Unknown"
         Quantity_Available = form.Quantity_Available.data
         price = form.price.data
         phone = current_user.phone if current_user.phone and current_user.phone.startswith("237") else f"237{current_user.phone}"
         new_food = FoodPosts(
            image=image_filename,
            restaurant_name=current_user.restaurant_name,
            name=name,
            Quantity_Available=Quantity_Available,
            location_name=location_name,
            status=status,
            latitude= 4.0511,  # Default latitude for Douala
            longitude= 9.7679, # Default longitude for Douala
            price = price,
            phone = phone,
            restaurant_id=current_user.id
        )
         
        db.session.add(new_food)
        db.session.commit()
        flash("Food added successfully!", "success")
        return redirect(url_for('restaurant.dashboard'))
    return render_template("food.html", form=form, title="Add Food")
 
@restauraunt_bp.route("/restaurants",methods=["GET","POST"])
@login_required
def dashboard():

    if current_user.role != "Restaurant":
        flash("Access denied! Only restaurants can view this page.", "danger")
        return redirect(url_for('auth.register'))
    
    foods = FoodPosts.query.filter_by(restaurant_id=current_user.id).all()
    pending_orders = OrderPosts.query.join(FoodPosts).filter(
        FoodPosts.restaurant_id == current_user.id,
        OrderPosts.order_status == "Pending"
    ).options(joinedload(OrderPosts.food), joinedload(OrderPosts.order)).all()

    return render_template("restaurant.html", foods=foods, pending_orders=pending_orders)


@restauraunt_bp.route("/restaurant/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_food(id):
    if current_user.role != "Restaurant":
        flash("Access denied!", "danger")
        return redirect(url_for('home'))
    
    # Find the food
    food = FoodPosts.query.filter_by(id=id, restaurant_id=current_user.id).first()
    if not food:
        flash("Food not found or access denied.", "danger")
        return redirect(url_for('restaurant.dashboard'))
    
    form = FoodForm()

    if request.method == "GET":
        form.Name.data = food.name
        form.Quantity_Available.data = food.Quantity_Available
        form.status.data = food.status
        form.location_name.data = food.location_name
        form.price.data = food.price

    if form.validate_on_submit():
        food.name = form.Name.data
        food.Quantity_Available = form.Quantity_Available.data
        food.status = form.status.data
        food.location_name = form.location_name.data or food.location_name
        food.price = form.price.data
        db.session.commit()
        flash("Food updated successfully!", "success")
        return redirect(url_for('restaurant.dashboard'))

    return render_template("update_food.html", form=form, food=food)

@restauraunt_bp.route("/restaurant/order/accept/<int:order_id>", methods=["POST"])
@login_required
def accept_order(order_id):
    if current_user.role != "Restaurant":
        flash("Access denied!", "danger")
        return redirect(url_for('restaurant.dashboard'))

    order = OrderPosts.query.join(FoodPosts).filter(
        OrderPosts.id == order_id,
        FoodPosts.restaurant_id == current_user.id,
        OrderPosts.order_status == "Pending"
    ).first()

    if not order:
        flash("Order not found or cannot be accepted.", "danger")
        return redirect(url_for('restaurant.dashboard'))

    order.order_status = "Accepted"
    order.accepted_at = datetime.utcnow()
    db.session.commit()
    flash("Order accepted successfully!", "success")
    return redirect(url_for('restaurant.dashboard'))

@restauraunt_bp.route("/restaurant/order/reject/<int:order_id>", methods=["POST"])
@login_required
def reject_order(order_id):
    if current_user.role != "Restaurant":
        flash("Access denied!", "danger")
        return redirect(url_for('restaurant.dashboard'))

    order = OrderPosts.query.join(FoodPosts).filter(
        OrderPosts.id == order_id,
        FoodPosts.restaurant_id == current_user.id,
        OrderPosts.order_status == "Pending"
    ).first()

    if not order:
        flash("Order not found or cannot be rejected.", "danger")
        return redirect(url_for('restaurant.dashboard'))

    order.order_status = "Rejected"
    order.food.Quantity_Available += order.quantity_ordered
    if order.food.Quantity_Available > 0 and order.food.status == "Sold Out":
        order.food.status = "Available"

    db.session.commit()
    flash("Order rejected successfully!", "success")
    return redirect(url_for('restaurant.dashboard'))