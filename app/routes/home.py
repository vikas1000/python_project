from flask import Blueprint, render_template
from sqlalchemy import func

from app.models import db
from app.models.employee import Employee

home_bp = Blueprint("home", __name__)

@home_bp.route("/home")
def home():
    total_employees   = Employee.query.count()
    total_departments = db.session.query(func.count(Employee.department.distinct())).scalar() or 0
    avg_salary        = db.session.query(func.avg(Employee.salary)).scalar()
    recent_employees  = Employee.query.order_by(Employee.id.desc()).limit(5).all()

    return render_template(
        "home.html",
        total_employees   = total_employees,
        total_departments = total_departments,
        avg_salary        = avg_salary,
        recent_employees  = recent_employees,
    )

@home_bp.route("/")
def index():
    return home()
