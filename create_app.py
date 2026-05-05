from app import app,db
import os
def create_app():
    
 if __name__ == "__main__":
    with app.app_context():
        db.create_all()
     
    app.run(debug=os.getenv("FLASK_DEBUG", "False").lower() == "true")
    return app