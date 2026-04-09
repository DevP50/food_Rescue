from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager

# Initialize the extensions without importing the Flask app directly
db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    restaurant_name = db.Column(db.String(100), nullable=True)
    restaurant_location = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(35), nullable=True)
    food_posts = db.relationship('FoodPosts', backref='restaurant', lazy=True)
    order_posts = db.relationship('OrderPosts', backref='username', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}', '{self.phone}')"

class FoodPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(100), nullable=True, default="default.jpg")
    name = db.Column(db.String(60), nullable=False)
    Quantity_Available = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    Available_until = db.Column(db.String(20), nullable=False, default=datetime.utcnow)
    location_name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food = db.relationship("OrderPosts", backref="name", lazy=True)

    def __repr__(self):
        return f"FoodPosts('{self.name}', '{self.Quantity_Available}', '{self.status}', '{self.Available_until}', '{self.location_name}')"

class OrderPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food_posts.id'), nullable=False)
