from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TimeField, SubmitField,PasswordField,HiddenField,FileField,BooleanField
from wtforms.validators import Length, DataRequired, NumberRange,Email, Optional,ValidationError


class FoodForm(FlaskForm):
    image = FileField("Image")
    Name = StringField("Food Name", validators=[DataRequired(), Length(min=3, max=60)])
    Quantity_Available = IntegerField("Quantity Available", validators=[DataRequired(), NumberRange(min=1)])
    status = SelectField("Status", choices=[("Available","Available"), ("Urgent","Urgent")])
    Available_until = TimeField("Available Until(Time)", format="%H:%M", validators=[DataRequired()])
    location_name = StringField('Location', render_kw={"readonly": True})
    latitude = HiddenField("Latitude")
    longitude = HiddenField("Longitude")
    submit = SubmitField("Add Food")

class RegisterForm(FlaskForm):
   username = StringField("Username",validators=[DataRequired(),Length(min=3, max=25)])
   email = StringField("Email", validators=[DataRequired(), Email()])
   password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=25)])
   Role = SelectField("Role",choices=[("User","User"),("Restaurant","Restaurant"),("Food Delivery","Food Delivery")])
   restaurant_name = StringField('Restaurant Name', validators=[Optional()])
   restaurant_location= SelectField("restaurant_location",choices=[("Bonamoussadi","Bonamoussadi"),("Bonapriso","Bonapriso"),("Bonaberi","Bonaberi"),("Akwa","Akwa")], validators=[Optional()])
   latitude = HiddenField("lat")
   longitude = HiddenField("lng")
   phone = StringField('Phone', validators=[DataRequired()])


   submit = SubmitField("Register")

   def validate_username(self, username):
       # Import here to avoid circular import
       from models import User
       user = User.query.filter_by(username=username.data).first()
       if user:
           raise ValidationError("This username is taken please choose another one")
    
   def validate_email(self, email):
       # Import here to avoid circular import
       from models import User
       user = User.query.filter_by(email=email.data).first()
       if user:
           raise ValidationError("This email is taken please choose another one")
                       

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=25)])
    Remember = BooleanField("Remember Me")

    submit = SubmitField("Login")

    
class RequestForm(FlaskForm):
    food_id = HiddenField("Food ID")
    Quantity_Ordered = IntegerField("Quantity Ordered", validators=[DataRequired(), NumberRange(min=1,max=2)])
    submit = SubmitField("Request Food")