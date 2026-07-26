import os

class Config:

    # Flask secret key — read from environment on Render, fallback for local dev
    SECRET_KEY = os.environ.get("SECRET_KEY", "ems-sha256-secret-key-2026")

    # Database — Render provides DATABASE_URL for MySQL/PostgreSQL add-ons.
    # For local XAMPP development the fallback is used automatically.
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "mysql+pymysql://root:@localhost:3306/employee_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_NAME  = "Employee Management System"
    DEBUG     = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
