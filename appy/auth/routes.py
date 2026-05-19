from flask import Blueprint, render_template, redirect, url_for, flash
from appy.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from appy.models.model import User
from flask_login import login_user, logout_user, current_user, login_required
from . import auth_bp
@auth_bp.route("/")
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
        form = RegisterForm()
        if form.validate_on_submit():
        # Hash the password before storing
         print(form.Password.data)
         hashed_password = generate_password_hash(form.Password.data)
        
        
        # Check if the role is Restaurant and validate required fields
         if form.Role.data == "Restaurant":
         
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
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"Registration failed: {str(e)}", "danger")
        return render_template("register.html", form=form)
    
  


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Check if user exists and password matches
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.Remember.data)
            return redirect(url_for('orders.homes'))
        else:
            flash("Invalid email or password.", "danger")   
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{field}: {error}", "danger")
                            
    return render_template('login.html',form=form)

