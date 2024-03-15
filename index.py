from flask import Flask, render_template
import os
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy.orm import sessionmaker
from models.user import User
from controllers.user import users_routes
from controllers.account import accounts_routes
from controllers.transaction import transaction_routes
from flask_login import LoginManager

from connectors.mysql_connector import  engine
from flask_jwt_extended import JWTManager

load_dotenv()

app= Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.getenv('SECRET_KEY')
jwt = JWTManager(app)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    connection = engine.connect()
    Session = sessionmaker(connection)
    session = Session()

    return session.query(User).get(int(user_id))
app.register_blueprint(users_routes)
app.register_blueprint(accounts_routes)
app.register_blueprint(transaction_routes)


@app.route("/")
def hello():
    return render_template("user/home.html")