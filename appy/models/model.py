from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, current_user

# Initialize the extensions without importing the Flask app directly
from extensions import db,login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    restaurant_name = db.Column(db.String(100), nullable=True)
    restaurant_location = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(35), nullable=True)
  
    food_posts = db.relationship('FoodPosts', backref='restaurant', lazy=True)
    order_posts = db.relationship('OrderPosts', backref='order', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}', '{self.phone}')"
    

class OrderPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food_posts.id'), nullable=True)

    food = db.relationship(
        "FoodPosts",
        back_populates="order_posts"
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    quantity_ordered = db.Column(db.Integer, nullable=True)
    accepted_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_status = db.Column(db.String(20), default="Pending", nullable=False)
    total_price = db.Column(db.Float, nullable=False)
   
class FoodPosts (db.Model):
    id = db.Column(db.Integer, primary_key=True)

    image = db.Column(db.String(100), nullable=True, default="default.jpg")
    restaurant_name = db.Column(db.String(100), nullable=True)
    name = db.Column(db.String(60), nullable=False)
    Quantity_Available = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Available")
   

    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    location_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    phone = db.Column(db.String(35), nullable=True) 
    restaurant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ✅ ONLY THIS ONE (keep it)
    order_posts = db.relationship(
        "OrderPosts",
        back_populates="food",
        lazy=True
    )

    @property
    def is_available(self):
        return self.Quantity_Available > 0 and self.status in ("Available", "Urgent")

    def __repr__(self):
        return f"FoodPosts('{self.name}', '{self.Quantity_Available}', '{self.status}', '{self.location_name}')"