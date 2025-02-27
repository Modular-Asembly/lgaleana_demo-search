from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.sql_adaptor import get_db
from app.note import Note

router = APIRouter()

@router.get("/notes/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)) -> dict:
    note = db.query(Note).filter(Note.id == note_id).first()
    if note is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Note with id {note_id} not found."
        )
    return {
        "id": note.id,
        "client_id": note.client_id,
        "date": note.date,
        "title": note.title,
        "content": note.content
    }
