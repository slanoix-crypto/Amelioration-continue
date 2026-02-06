from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Employee, Improvement
from ._common import templates

router = APIRouter(prefix="/admin")

@router.get("")
def admin_home(request: Request, db: Session = Depends(get_db)):
    employees = db.query(Employee).order_by(Employee.active.desc(), Employee.name.asc()).all()
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "active_tab": "admin",
            "current_month_label": "",
            "monthly_goal": 0,
            "employees": employees,
        },
    )

@router.post("/employees")
def add_employee(name: str = Form(...), db: Session = Depends(get_db)):
    name = name.strip()
    if name:
        existing = db.query(Employee).filter(Employee.name == name).first()
        if not existing:
            db.add(Employee(name=name, active=True))
            db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/employees/{employee_id}/toggle")
def toggle_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.get(Employee, employee_id)
    if emp:
        emp.active = not emp.active
        db.commit()
    return RedirectResponse(url="/admin", status_code=303)

@router.post("/employees/{employee_id}/delete")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    emp = db.get(Employee, employee_id)
    if not emp:
        return RedirectResponse(url="/admin", status_code=303)

    # Sécurité : si l'employé est référencé dans des améliorations, on ne supprime pas
    used_as_creator = db.query(Improvement).filter(Improvement.created_by_employee_id == employee_id).count()
    used_as_assignee = db.query(Improvement).filter(Improvement.assigned_to_employee_id == employee_id).count()

    if used_as_creator > 0 or used_as_assignee > 0:
        # on refuse la suppression; l'utilisateur peut "désactiver" à la place
        return RedirectResponse(url="/admin?error=linked", status_code=303)

    db.delete(emp)
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)
