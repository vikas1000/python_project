import os
from flask import Flask
from config import Config

from app.routes.employee import employee_bp
from app.routes.department import department_bp
from app.routes.home import home_bp

from app.models import db
from flask_migrate import Migrate

migrate = Migrate()

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)

    # Render injects DATABASE_URL as postgres://... — SQLAlchemy needs postgresql://
    db_url = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    if db_url.startswith("postgres://"):
        app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace("postgres://", "postgresql://", 1)

    # initialize database
    db.init_app(app)

    # flask-migrate
    migrate.init_app(app, db)

    app.register_blueprint(home_bp)
    app.register_blueprint(employee_bp)
    app.register_blueprint(department_bp)

    # Auto-create all tables on startup (works on both local and Render)
    with app.app_context():
        db.create_all()

    return app
