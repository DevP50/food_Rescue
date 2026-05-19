import os
from datetime import datetime
import time
import logging
from flask import Flask, abort, render_template, request, url_for, redirect, flash, Blueprint
from sqlalchemy.orm import joinedload
from extensions import db, login_manager
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from appy.auth.routes import auth_bp
from appy.restaurant.routes import restauraunt_bp
from appy.admin.routes import admin_bp
from appy.users.routes import users
from appy.orders.routes import order_bp
from flask_migrate import Migrate
from config import get_config

app = Flask(__name__)
app.config.from_object(get_config())
app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
app.config.setdefault("WTF_CSRF_ENABLED", True)

admin_email = app.config.get("ADMIN_EMAIL")

  
 #Database secrets should be stored in environment variables or a config file, not hardcoded in the codebase for security reasons. This is just for demonstration purposes.
db.init_app(app)#To avoid circular imports, we initialize the database and login manager here instead of in models.py
login_manager.init_app(app)#This tells Flask-Login which view to redirect to when a user tries to access a protected route without being logged in. It also sets the category for the flash message that appears when a user is redirected to the login page.
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
#Every class is a table in the database, and every object of the class is a column in the table.
# Removed in-memory lists and orders - now using database models
# Setup logging
logging.basicConfig(level=logging.INFO)
app.logger.setLevel(logging.INFO)
migrate = Migrate(app, db)

app.register_blueprint(auth_bp)#Register the Created blueprint for each package
app.register_blueprint(restauraunt_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(users)
app.register_blueprint(order_bp ,url_prefix="/orders")

  
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.errorhandler(404)
def page_not_found(e):#Custom Error Pages (The app calls the error_handler method and the error code is pass as an argument and executes the function

    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=app.config.get("DEBUG", False))




