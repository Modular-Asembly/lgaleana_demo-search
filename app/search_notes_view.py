from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session

from app.sql_adaptor import get_db
from app.note import Note
from sqlalchemy import and_
from fastapi.concurrency import run_in_threadpool

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def search_notes_logic(
    db: Session, 
    client_id: Optional[int], 
    start_date: Optional[datetime], 
    end_date: Optional[datetime]
) -> List[dict]:
    filters = []
    if client_id is not None:
        filters.append(Note.client_id == client_id)
    if start_date is not None:
        filters.append(Note.date >= start_date)
    if end_date is not None:
        filters.append(Note.date <= end_date)
    
    query = db.query(Note)
    if filters:
        query = query.filter(and_(*filters))
    notes = query.all()
    result = [
        {
            "id": note.id,
            "client_id": note.client_id,
            "date": note.date,
            "title": note.title,
            "content": note.content
        }
        for note in notes
    ]
    return result

async def run_search_notes(
    db: Session, 
    client_id: Optional[int], 
    start_date: Optional[datetime], 
    end_date: Optional[datetime]
) -> List[dict]:
    return await run_in_threadpool(search_notes_logic, db, client_id, start_date, end_date)

@router.get("/notes/search/view", response_class=HTMLResponse)
async def get_search_notes_view(request: Request):
    # Render the template with no search results initially
    return templates.TemplateResponse("search_notes.html", {"request": request, "results": None})

@router.post("/notes/search/view", response_class=HTMLResponse)
async def post_search_notes_view(
    request: Request,
    client_id: Optional[int] = Form(None),
    start_date: Optional[str] = Form(None),
    end_date: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    # Convert form date strings to datetime objects if provided.
    try:
        start_dt = datetime.fromisoformat(start_date) if start_date else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid format for start date. Use ISO format (YYYY-MM-DDTHH:MM:SS).")
    try:
        end_dt = datetime.fromisoformat(end_date) if end_date else None
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid format for end date. Use ISO format (YYYY-MM-DDTHH:MM:SS).")
    
    results = await run_search_notes(db, client_id, start_dt, end_dt)
    return templates.TemplateResponse("search_notes.html", {"request": request, "results": results})
