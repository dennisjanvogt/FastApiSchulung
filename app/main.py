import logging
from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse

from app.api.api_v1.api import api_router
from app.core.auth import get_current_user
from app.config import settings
from app.db.init_db import init_db
from app.db.session import get_db
from app.models.user import User

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# App erstellen
app = FastAPI(
    title="Bücherverwaltung API",
    description="API für die Verwaltung von Büchern",
    version="1.0.0",
)

# Static files und Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# CORS-Middleware hinzufügen
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API-Router einbinden
app.include_router(api_router, prefix=settings.API_V1_STR)


# Root-Seite
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return RedirectResponse(url="/books")


# Login-Seite
@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Bücher-Seite
@app.get("/books", response_class=HTMLResponse)
async def read_books(request: Request):
    return templates.TemplateResponse("books.html", {"request": request})


# Startup-Event
@app.on_event("startup")
def on_startup():
    logger.info("Starte Anwendung...")
    db = next(get_db())
    init_db(db)
    logger.info("Datenbank initialisiert")


# Shutdown-Event
@app.on_event("shutdown")
def on_shutdown():
    logger.info("Anwendung wird heruntergefahren...")


# Fehlerbehhandlung
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unerwarteter Fehler: {exc}", exc_info=True)
    return templates.TemplateResponse(
        "error.html",
        {"request": request, "error": "Ein unerwarteter Fehler ist aufgetreten."},
        status_code=500,
    )

@app.get("/debug", include_in_schema=False)
async def debug_info():
    """
    Debug-Informationen für Entwicklungszwecke.
    Nicht in Produktion verwenden!
    """
    return {
        "app_settings": {
            "api_v1_str": settings.API_V1_STR,
            "backend_cors_origins": settings.BACKEND_CORS_ORIGINS,
            "sqlalchemy_database_uri": settings.SQLALCHEMY_DATABASE_URI.replace(
                settings.FIRST_SUPERUSER_PASSWORD, "***"
            ) if settings.FIRST_SUPERUSER_PASSWORD in settings.SQLALCHEMY_DATABASE_URI else settings.SQLALCHEMY_DATABASE_URI,
        },
        "environment": {
            "python_version": platform.python_version(),
            "system": platform.system(),
        }
    }

# Vergessen Sie nicht, platform zu importieren:
import platform


# app/main.py (nur den letzten Teil aktualisieren)
if __name__ == "__main__":
    import uvicorn
    
    # Für Produktion
    # host = "127.0.0.1"
    
    # Für Entwicklung (alle Interfaces)
    host = "0.0.0.0"
    
    port = 8888
    
    print(f"Server startet auf http://{host}:{port}")
    print(f"API-Dokumentation verfügbar unter http://{host}:{port}/docs")
    
    # Debug-Modus für Entwicklung
    uvicorn.run(app, host=host, port=port, log_level="debug")