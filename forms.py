from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TimeField, SubmitField
from wtforms.validators import Length, DataRequired, NumberRange

class FoodForm(FlaskForm):
    Name = StringField("Name", validators=[DataRequired(), Length(min=3, max=60)])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])
    location = StringField("Where is the food", validators=[DataRequired(), Length(min=5, max=35)])
    status = SelectField("Status", choices=[("Available","Available"), ("Urgent","Urgent")])
    Available_until = TimeField("Available Until(Time)", format="%H:%M", validators=[DataRequired()])
    submit = SubmitField("Add Food")



