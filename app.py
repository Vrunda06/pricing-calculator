 
from flask import Flask
from flask_jwt_extended import JWTManager
from models import db, Company, Tool, Section, Component
from routes import api_routes

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize the database and JWT Manager
db.init_app(app)
jwt = JWTManager(app)

# Register API routes
app.register_blueprint(api_routes)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
