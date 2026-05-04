from flask import Blueprint
order_bp = Blueprint("orders",__name__)
from . import routes