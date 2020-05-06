import os

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def create_app():

    app = Flask(__name__)

    # Configure session to use filesystem
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    Session(app)

    with app.app_context():
        db.execute("CREATE SCHEMA IF NOT EXISTS public")
        db.execute("CREATE TABLE IF NOT EXISTS users (id serial PRIMARY KEY, username varchar(60) UNIQUE NOT NULL, password varchar(240) NOT NULL)")
        db.execute("CREATE TABLE IF NOT EXISTS reviews (id serial PRIMARY KEY, isbn varchar(60) NOT NULL REFERENCES books(isbn), username varchar(60) UNIQUE NOT NULL, rating int NOT NULL, review varchar(1200) NOT NULL)")
        db.commit()

        from .auth import routes as auth_routes
        app.register_blueprint(auth_routes.bp)
        from .main import routes as main_routes
        app.register_blueprint(main_routes.bp)

        return app
