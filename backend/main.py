from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
import schemas
from utils import find_free_slots

app = FastAPI()

# ✅ CORS (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=engine)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "OpenSlots Backend Running"}


# ✅ CREATE
@app.post("/timetable", response_model=schemas.TimetableResponse)
def create_entry(entry: schemas.TimetableCreate, db: Session = Depends(get_db)):
    db_entry = models.TimetableEntry(**entry.model_dump())
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


# ✅ READ
@app.get("/timetable")
def get_entries(db: Session = Depends(get_db)):
    return db.query(models.TimetableEntry).all()


# ✅ DELETE
@app.delete("/timetable/{id}")
def delete_entry(id: int, db: Session = Depends(get_db)):
    entry = db.query(models.TimetableEntry).filter(models.TimetableEntry.id == id).first()

    if not entry:
        return {"error": "Entry not found"}

    db.delete(entry)
    db.commit()
    return {"message": "Deleted successfully"}


# ✅ UPDATE
@app.put("/timetable/{id}")
def update_entry(id: int, updated: schemas.TimetableCreate, db: Session = Depends(get_db)):
    entry = db.query(models.TimetableEntry).filter(models.TimetableEntry.id == id).first()

    if not entry:
        return {"error": "Entry not found"}

    entry.subject = updated.subject
    entry.day = updated.day
    entry.start_time = updated.start_time
    entry.end_time = updated.end_time
    entry.room = updated.room

    db.commit()
    db.refresh(entry)
    return entry


# ✅ FREE SLOTS + FILTER
@app.get("/free-slots")
def get_free_slots(day: str = None, db: Session = Depends(get_db)):
    entries = db.query(models.TimetableEntry).all()

    if day:
        entries = [e for e in entries if e.day == day]

    return find_free_slots(entries)