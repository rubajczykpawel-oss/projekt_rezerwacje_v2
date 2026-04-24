from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from security import create_access_token, verify_access_token, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, engine, Base
import models
import schemas
import crud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Baza działa V2"}


@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = crud.get_user_by_username(db, user.username)

    if existing_user:
        raise HTTPException(status_code=400, detail="Taki użytkownik już istnieje")

    new_user = crud.create_user(db, user)
    return new_user


@app.post("/login")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, form_data.username)

    if not db_user:
        raise HTTPException(status_code=400, detail="Nie ma takiego użytkownika")

    from auth import verify_password

    if not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Złe hasło")

    access_token = create_access_token(data={"sub": db_user.email})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = verify_access_token(token)

    user = crud.get_user_by_email(db, email)

    if not user:
        raise HTTPException(status_code=404, detail="Użytkownik nie istnieje")

    return user


@app.get("/profile")
def read_profile(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email
    }

@app.post("/reservations", response_model=schemas.ReservationResponse)
def create_reservation(
    reservation: schemas.ReservationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.create_reservation(db, reservation, current_user.id)


@app.get("/reservations")
def get_reservations(
    date: str | None = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_user_reservations(db, current_user.id, date)

@app.put("/reservations/{reservation_id}", response_model=schemas.ReservationResponse)
def update_reservation(
    reservation_id: int,
    reservation: schemas.ReservationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated = crud.update_reservation(db, reservation_id, reservation, current_user.id)

    if not updated:
        raise HTTPException(status_code=404, detail="Nie znaleziono rezerwacji")

    return updated


@app.delete("/reservations/{reservation_id}")
def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted = crud.delete_reservation(db, reservation_id, current_user.id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Nie znaleziono rezerwacji")

    return {"message": "Usunięto rezerwację"}

@app.get("/reservations/{reservation_id}", response_model=schemas.ReservationResponse)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    reservation = crud.get_reservation_by_id(db, reservation_id, current_user.id)

    if not reservation:
        raise HTTPException(status_code=404, detail="Nie znaleziono rezerwacji")

    return reservation

