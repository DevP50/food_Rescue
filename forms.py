from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TimeField, SubmitField,PasswordField,HiddenField,FileField,BooleanField
from wtforms.validators import Length, DataRequired, NumberRange,Email, Optional

class FoodForm(FlaskForm):
    image = FileField("Image")
    Name = StringField("Restaurant Name", validators=[DataRequired(), Length(min=3, max=60)])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])
    status = SelectField("Status", choices=[("Available","Available"), ("Urgent","Urgent")])
    Available_until = TimeField("Available Until(Time)", format="%H:%M", validators=[DataRequired()])
    location_name = StringField('Location', render_kw={"readonly": True})
    latitude = HiddenField("Latitude")
    longitude = HiddenField("Longitude")
    submit = SubmitField("Add Food")

class RegistrationForm(FlaskForm):
   username = StringField("Username",validators=[DataRequired(),Length(min=3, max=25)])
   email = StringField("Email", validators=[DataRequired(), Email()])
   password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=25)])
   Role = SelectField("Role",choices=[("User","User"),("Restaurant","Restaurant"),("Food Delivery","Food Delivery")])
   restaurant_name = StringField('Restaurant Name', validators=[Optional()])
   Location= SelectField("Location",choices=[("Bonamoussadi","Bonamoussadi"),("Bonapriso","Bonapriso"),("Bonaberi","Bonaberi"),("Akwa","Akwa")], validators=[Optional()])
   phone = StringField('Phone', validators=[Optional()])

   submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=25)])
    Remember = BooleanField("Remember Me")

    submit = SubmitField("Login")

class RequestForm(FlaskForm):
    Quantity_Ordered = SelectField("Quantity Ordered", validators=[DataRequired(), NumberRange(min=1,max=2)])
    submit = SubmitField("Request Food")

   