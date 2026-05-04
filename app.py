import os
from datetime import datetime
import time
from flask import Flask, abort, render_template, request, url_for, redirect, flash,Blueprint
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
from config import SECRET_KEY,BASE_DIR,SQLALCHEMY_DATABASE_URI
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
BASE_DIR = BASE_DIR
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
from config import admin_email #Database secrets should be stored in environment variables or a config file, not hardcoded in the codebase for security reasons. This is just for demonstration purposes.
db.init_app(app)#To avoid circular imports, we initialize the database and login manager here instead of in models.py
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
#Every class is a table in the database, and every object of the class is a column in the table.
# Removed in-memory lists and orders - now using database models

migrate = Migrate(app, db)

app.register_blueprint(auth_bp)
app.register_blueprint(restauraunt_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(users)
app.register_blueprint(order_bp ,url_prefix="/orders")




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
     
    app.run(debug=True)
