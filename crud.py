from sqlalchemy.orm import Session
import models
import schemas
from auth import hash_password


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_reservations(db: Session, user_id: int, date: str | None = None):
    query = db.query(models.Reservation).filter(models.Reservation.user_id == user_id)

    if date:
        query = query.filter(models.Reservation.reservation_date == date)

    return query.all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pw
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def create_reservation(db: Session, reservation: schemas.ReservationCreate, user_id: int):
    new_reservation = models.Reservation(
        customer_name=reservation.customer_name,
        reservation_date=reservation.reservation_date,
        reservation_time=reservation.reservation_time,
        guests_count=reservation.guests_count,
        user_id=user_id
    )

    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    return new_reservation

def update_reservation(db: Session, reservation_id: int, reservation: schemas.ReservationCreate, user_id: int):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    if not db_reservation:
        return None

    if db_reservation.user_id != user_id:
        return None
    
    db_reservation.customer_name = reservation.customer_name
    db_reservation.reservation_date = reservation.reservation_date
    db_reservation.reservation_time = reservation.reservation_time
    db_reservation.guests_count = reservation.guests_count

    db.commit()
    db.refresh(db_reservation)

    return db_reservation

def delete_reservation(db: Session, reservation_id: int, user_id: int):
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()

    if not db_reservation:
        return None
    
    db.delete(db_reservation)
    db.commit()

    return db_reservation

def get_reservation_by_id(db: Session, reservation_id: int, user_id: int):
    return db.query(models.Reservation).filter(
        models.Reservation.id == reservation_id,
        models.Reservation.user_id == user_id
    ).first()
    