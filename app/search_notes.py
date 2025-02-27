from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.sql_adaptor import get_db
from app.note import Note

router = APIRouter()

@router.get("/notes/search", status_code=status.HTTP_200_OK)
def search_notes(
    client_id: Optional[int] = Query(None, description="Filter by client ID"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date (inclusive)"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date (inclusive)"),
    db: Session = Depends(get_db)
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
