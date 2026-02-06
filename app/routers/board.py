from datetime import datetime
from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/")
def board(request: Request):
    from app.main import templates
    
    now = datetime.now()
    current_month_label = now.strftime("%B %Y")
    monthly_goal = 10  # temporaire (viendra de l'Admin)

    return templates.TemplateResponse(
        "board.html",
        {
            "request": request,
            "active_tab": "tableau",
            "current_month_label": current_month_label,
            "monthly_goal": monthly_goal,
        },
    )
