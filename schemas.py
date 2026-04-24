from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


class ReservationCreate(BaseModel):
    customer_name: str
    reservation_date: str
    reservation_time: str
    guests_count: int

    @field_validator("customer_name", "reservation_date", "reservation_time")
    @classmethod
    def fields_not_empty(cls, value):
        if value.strip() == "":
            raise ValueError("Pole nie może być puste")
        return value

    @field_validator("guests_count")
    @classmethod
    def guests_count_positive(cls, value):
        if value <= 0:
            raise ValueError("Liczba gości musi być większa od 0")
        return value

class ReservationResponse(BaseModel):
    id: int
    customer_name: str
    reservation_date: str
    reservation_time: str
    guests_count: int

    class Config:
        from_attributes = True