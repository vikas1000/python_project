from flask import Blueprint, request, redirect, url_for, render_template, flash
from sqlalchemy import asc, desc

from app.models.employee import Employee
from app.models import db

employee_bp = Blueprint("employee", __name__)

# ---------------------------------------------------------------------------
# Helper: build a query-string dict that preserves all active filters/search
# ---------------------------------------------------------------------------
def _current_params(**overrides):
    """Return a dict of the current request args, with any overrides applied."""
    params = {
        "search":     request.args.get("search", "").strip(),
        "department": request.args.get("department", "").strip(),
        "min_salary": request.args.get("min_salary", "").strip(),
        "max_salary": request.args.get("max_salary", "").strip(),
        "sort_by":    request.args.get("sort_by", "name"),
        "sort_dir":   request.args.get("sort_dir", "asc"),
        "page":       request.args.get("page", 1, type=int),
    }
    params.update(overrides)
    return params


# ---------------------------------------------------------------------------
# Employee List — with search, filter, sort, pagination
# ---------------------------------------------------------------------------
PER_PAGE = 10

@employee_bp.route("/employee/list")
def employee_list():
    search     = request.args.get("search", "").strip()
    department = request.args.get("department", "").strip()
    min_salary = request.args.get("min_salary", "").strip()
    max_salary = request.args.get("max_salary", "").strip()
    sort_by    = request.args.get("sort_by", "name")
    sort_dir   = request.args.get("sort_dir", "asc")
    page       = request.args.get("page", 1, type=int)

    # --- base query ---
    query = Employee.query

    # --- searching ---
    if search:
        like = f"%{search}%"
        query = query.filter(
            db.or_(
                Employee.name.ilike(like),
                Employee.email.ilike(like),
                Employee.department.ilike(like),
            )
        )

    # --- department filter ---
    if department:
        query = query.filter(Employee.department.ilike(f"%{department}%"))

    # --- salary range filter ---
    if min_salary:
        try:
            query = query.filter(Employee.salary >= float(min_salary))
        except ValueError:
            pass
    if max_salary:
        try:
            query = query.filter(Employee.salary <= float(max_salary))
        except ValueError:
            pass

    # --- sorting ---
    sort_columns = {
        "name":       Employee.name,
        "email":      Employee.email,
        "department": Employee.department,
        "salary":     Employee.salary,
    }
    col = sort_columns.get(sort_by, Employee.name)
    order_fn = asc if sort_dir == "asc" else desc
    query = query.order_by(order_fn(col))

    # --- total before pagination ---
    total = query.count()

    # --- pagination ---
    pagination = query.paginate(page=page, per_page=PER_PAGE, error_out=False)
    employees  = pagination.items

    # --- distinct departments for the filter drop-down ---
    all_departments = [
        row[0] for row in db.session.query(Employee.department).distinct().order_by(Employee.department).all()
    ]

    return render_template(
        "employee.html",
        employees       = employees,
        pagination      = pagination,
        total           = total,
        search          = search,
        department      = department,
        min_salary      = min_salary,
        max_salary      = max_salary,
        sort_by         = sort_by,
        sort_dir        = sort_dir,
        all_departments = all_departments,
        per_page        = PER_PAGE,
    )


# ---------------------------------------------------------------------------
# Add employee
# ---------------------------------------------------------------------------
@employee_bp.route("/employee/add", methods=["POST", "GET"])
def employeeAdd():
    if request.method == "POST":
        try:
            employee = Employee(
                name       = request.form["name"],
                email      = request.form["email"],
                password   = request.form["password"],
                salary     = float(request.form["salary"]),
                department = request.form["department"],
            )
            db.session.add(employee)
            db.session.commit()
            flash("Employee added successfully!", "success")
            return redirect(url_for("employee.employee_list"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding employee: {str(e)}", "danger")

    return render_template("add_employee.html")


# ---------------------------------------------------------------------------
# Employee detail
# ---------------------------------------------------------------------------
@employee_bp.route("/employee/employeeDetail/<int:id>", methods=["GET"])
def employeeDetail(id):
    employee = Employee.query.get_or_404(id)
    return render_template("employee_detail.html", employee=employee)


# ---------------------------------------------------------------------------
# Update employee
# ---------------------------------------------------------------------------
@employee_bp.route("/employee/employeeUpdate/<int:id>", methods=["POST", "GET"])
def employeeUpdate(id):
    employee = Employee.query.get_or_404(id)

    if request.method == "POST":
        try:
            employee.name       = request.form["name"]
            employee.email      = request.form["email"]
            employee.password   = request.form["password"]
            employee.salary     = float(request.form["salary"])
            employee.department = request.form["department"]
            db.session.commit()
            flash("Employee updated successfully!", "success")
            return redirect(url_for("employee.employee_list"))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating employee: {str(e)}", "danger")

    return render_template("update_employee.html", employee=employee)


# ---------------------------------------------------------------------------
# Delete employee
# ---------------------------------------------------------------------------
@employee_bp.route("/employee/employeeDelete/<int:id>")
def employeeDelete(id):
    employee = Employee.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        flash("Employee deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting employee: {str(e)}", "danger")
    return redirect(url_for("employee.employee_list"))


# ---------------------------------------------------------------------------
# Legacy / misc routes kept for compatibility
# ---------------------------------------------------------------------------
@employee_bp.route("/employee/<int:id>/<string:name>")
def searchByNameId(id, name):
    return f"ID : {id} Name : {name}"

@employee_bp.route("/employee")
def displaySpecific():
    department = request.args.get("department")
    page       = request.args.get("page")
    return f"Department : {department} Page : {page}"

@employee_bp.route("/employeeDepartment")
def gotodept():
    return redirect(url_for("department.departmentHome"))
