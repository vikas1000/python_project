from flask import Blueprint, render_template
from sqlalchemy import func

from app.models import db
from app.models.employee import Employee

department_bp = Blueprint("department", __name__)

@department_bp.route("/department")
def departmentHome():
    # Returns list of (department_name, employee_count, avg_salary)
    departments = (
        db.session.query(
            Employee.department,
            func.count(Employee.id).label("count"),
            func.avg(Employee.salary).label("avg_salary"),
        )
        .group_by(Employee.department)
        .order_by(Employee.department)
        .all()
    )
    return render_template("department.html", departments=departments)
