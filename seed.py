users = [
    {"email": "admin@nowasteam.com", "password": "1234", "role": "admin"},
    {"email": "resto1@gmail.com", "password": "1234", "role": "restaurant"},
    {"email": "resto2@gmail.com", "password": "1234", "role": "restaurant"},
    {"email": "user1@gmail.com", "password": "1234", "role": "user"},
    {"email": "user2@gmail.com", "password": "1234", "role": "user"},
]

food_posts = [
    {
        "title": "Rice and Stew",
        "quantity": 5,
        "price": 500,
        "location": "Bonamoussadi",
        "restaurant_email": "resto1@gmail.com"
    },
    {
        "title": "Jollof Rice",
        "quantity": 3,
        "price": 700,
        "location": "Akwa",
        "restaurant_email": "resto1@gmail.com"
    },
    {
        "title": "Grilled Chicken",
        "quantity": 4,
        "price": 1000,
        "location": "Deido",
        "restaurant_email": "resto2@gmail.com"
    }
]


orders = [
    {
        "user_email": "user1@gmail.com",
        "food_title": "Rice and Stew",
        "quantity": 1,
        "status": "requested"
    },
    {
        "user_email": "user2@gmail.com",
        "food_title": "Jollof Rice",
        "quantity": 1,
        "status": "requested"
    },
    {
        "user_email": "user1@gmail.com",
        "food_title": "Grilled Chicken",
        "quantity": 1,
        "status": "delivered"
    }
]

ists=  [ 
      {
          "image": "burger.jpg",
        "Name": "TCHOP ET YAMO",
        "Quantity_Available": 5,
        "longitude": "4.6",
        "latitude": "4.04",
        "location_name": "Bonamoussadi",  # Add location field
        "status": "available",
        "Available_until": "18:00",
        "food_name": "Egusi Soup",
        "id" : 0
         },
         {
            "Name": "TCHOP ET YAMO",
            "Quantity_Available": 5,
            "longitude": "4.6",
            "latitude": "4.04",
            "location_name": "Bonamoussadi",  # Add location field
             "status": "available",
             "Available_until": "18:00",
            "food_name": "Beignet et Haricot",
            "id" : 1
         }
]