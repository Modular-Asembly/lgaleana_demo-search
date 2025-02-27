from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.sql_adaptor import get_db
from app.note import Note

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/notes/{note_id}/view", response_class=HTMLResponse)
def display_note_view(note_id: int, request: Request, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail=f"Note with id {note_id} not found.")
    return templates.TemplateResponse("display_note.html", {"request": request, "note": note})
