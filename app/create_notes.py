from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.sql_adaptor import get_db
from app.note import Note

router = APIRouter()

class CreateNoteRequest(BaseModel):
    client_id: int = Field(..., description="Client's identifier")
    date: datetime = Field(default_factory=datetime.utcnow, description="Date of the note")
    title: str = Field(..., description="Title of the note")
    content: str = Field(None, description="Content of the note")

@router.post("/notes", status_code=status.HTTP_201_CREATED)
def create_note(note_in: CreateNoteRequest, db: Session = Depends(get_db)) -> dict:
    # Create a new Note instance using the provided data
    new_note = Note(
        client_id=note_in.client_id,
        date=note_in.date,
        title=note_in.title,
        content=note_in.content
    )
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    # Return the created note details as a dict
    return {
        "id": new_note.id,
        "client_id": new_note.client_id,
        "date": new_note.date,
        "title": new_note.title,
        "content": new_note.content
    }
