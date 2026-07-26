class Config:

    SECRET_KEY = "ems-sha256-secret-key-2026"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost:3306/employee_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_NAME = "Employee Management System"
    UPLOAD_FOLDER = "uploads"
    API_KEY = "12341asdasd"
    DEBUG = True
