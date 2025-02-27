from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.sql_adaptor import engine, Base
from app.search_notes import router as search_notes_router
from app.create_notes import router as create_notes_router
from app.get_note import router as get_note_router
from app.search_notes_view import router as search_notes_view_router
from app.display_note_view import router as display_note_view_router

def create_app() -> FastAPI:
    app = FastAPI(title="Notes Service", description="FastAPI service for managing notes.", version="1.0.0")

    # Add CORS middleware to allow all origins.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include all routers from the application.
    app.include_router(search_notes_router)
    app.include_router(create_notes_router)
    app.include_router(get_note_router)
    app.include_router(search_notes_view_router)
    app.include_router(display_note_view_router)

    # Create all database tables.
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as e:
        # Let errors raise as specified.
        raise e

    return app

app = create_app()
