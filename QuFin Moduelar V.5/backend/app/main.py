
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

load_dotenv()

from .routers import auth, payments

from .db import Base, engine


app = FastAPI(title="QuFin Backend")

# Mount static files for QuFin Moduelar V.5 at /QuFin Moduelar V.5
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
app.mount("/QuFin Moduelar V.5", StaticFiles(directory=static_dir, html=True), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://localhost:8000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])

@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup():
    # create tables from SQLAlchemy models (development-friendly)
    getattr(Base, 'metadata').create_all(bind=engine)

