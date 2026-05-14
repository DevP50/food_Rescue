import datetime

from sqlalchemy import func

from sqlalchemy import func

from appy.models.model import OrderPosts
DAILY_LIMIT = 5
PER_RESTAURANT_DAILY_LIMIT = 3

def check_order_limit(user_id, restaurant_id,quantity=1):
    today = datetime.utcnow().date()
    user_orders_today = OrderPosts.query(
        func.coal(func.sum(OrderPosts.quantity_ordered), 0)).filter(
        OrderPosts.order_id == user_id, 
        func.date(OrderPosts.created_at) == today, 
        OrderPosts.order_status != "Rejected"
    ).scalar()#Sum the total quantity ordered by a specific user today whose other status is not rejected, and default to 0 if there are no orders. This ensures that we only count valid orders towards the user's daily limit.
    total_portions_today = sum(o.quantity_ordered for o in user_orders_today)
    restaurants_today = {o.food.restaurant_id for o in user_orders_today if o.food}# Get the set of restaurants the user ordered from today

    if total_portions_today + quantity > DAILY_LIMIT:
        return False, "You have reached your daily limit of 5 portions."

    if restaurant_id in restaurants_today and total_portions_today + quantity > PER_RESTAURANT_DAILY_LIMIT:
        return False, "You can only request up to 3 portions from the same restaurant per day."

    return True, ""
