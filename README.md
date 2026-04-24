# 📅 System rezerwacji (FastAPI + SQLite)

## 📌 Opis projektu

Aplikacja webowa umożliwiająca zarządzanie rezerwacjami użytkowników.
System pozwala na rejestrację, logowanie oraz wykonywanie operacji CRUD na rezerwacjach.

Projekt został wykonany w technologii **Python + FastAPI + SQLite**.

---

## ⚙️ Technologie

* Python 3
* FastAPI
* SQLAlchemy (ORM)
* SQLite (baza danych)
* JWT (autoryzacja)
* HTML + JavaScript (frontend)
* Uvicorn (serwer)

---

## 🔐 Funkcjonalności

### 👤 Użytkownicy

* Rejestracja użytkownika
* Logowanie użytkownika
* Hashowanie haseł (bcrypt)
* Autoryzacja JWT

---

### 📅 Rezerwacje (CRUD)

| Operacja | Endpoint                  | Opis                         |
| -------- | ------------------------- | ---------------------------- |
| CREATE   | POST /reservations        | Dodanie rezerwacji           |
| READ     | GET /reservations         | Lista rezerwacji użytkownika |
| READ     | GET /reservations/{id}    | Szczegóły rezerwacji         |
| UPDATE   | PUT /reservations/{id}    | Edycja rezerwacji            |
| DELETE   | DELETE /reservations/{id} | Usunięcie rezerwacji         |

---

## 🧠 Dodatkowe funkcje

* Walidacja danych (Pydantic)
* Filtrowanie rezerwacji po dacie:

GET /reservations?date=2026-05-01

* Ochrona endpointów (JWT)
* Użytkownik widzi tylko swoje dane

---

## 🗄️ Struktura projektu

projekt_rezerwacje_v2/
│
├── app.py
├── models.py
├── schemas.py
├── crud.py
├── database.py
├── auth.py
├── security.py
├── rezerwacje.db
├── index.html
└── README.md

---

## 🚀 Uruchomienie projektu

### 1. Instalacja zależności

pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose

---

### 2. Uruchomienie backendu

uvicorn app:app --reload

---

### 3. Swagger (test API)

http://localhost:8000/docs

---

### 4. Frontend

Otwórz plik:

index.html

lub użyj:

Live Server w VS Code

---

## 🔑 Dane testowe

login: pawel
hasło: haslo123

---

## 🧪 Przykład rezerwacji

{
"customer_name": "Jan Kowalski",
"reservation_date": "2026-05-01",
"reservation_time": "18:00",
"guests_count": 4
}

---

## 🧑‍💻 Autor

Projekt wykonany w ramach zajęć z  baz danych.

---

## 📌 Podsumowanie

Aplikacja implementuje pełny system:

* autoryzacji użytkownika (JWT)
* operacji CRUD
* pracy z bazą danych
* prostego frontendu

Projekt odzwierciedla typową architekturę aplikacji backendowej REST API.
