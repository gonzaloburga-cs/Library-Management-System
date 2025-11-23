#!/usr/bin/env python3

from fastapi import FastAPI, Depends, Request, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from supabase import create_client
import os

load_dotenv()

# Environment variables
SUPABASE_DB_URL = os.getenv("SUPABASE_DATABASE_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_PUBLIC_KEY = os.getenv("SUPABASE_PUBLIC_KEY")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

# Database setup
engine = create_engine(SUPABASE_DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Supabase clients
supabase = create_client(SUPABASE_URL, SUPABASE_PUBLIC_KEY)
supabase_service_client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

# FastAPI app
app = FastAPI()


# Dependency for database session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def hello_world():
    """Test function to check server connectivity."""
    return {"message": "Hello World"}


@app.get("/books")
def get_books():
    """Return a list of all books."""
    response = supabase.table("books").select("*").execute()
    return response.data


@app.post("/my-books")
async def get_my_books(request: Request):
    """Return books currently checked out by a user."""
    data = await request.json()
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token required")
    
    supabase.postgrest.auth(auth_token)

    query = """
    SELECT id, title, author, isbn
    FROM books
    WHERE id IN (
        SELECT book_id
        FROM checkout_logs
        WHERE checkin_date IS NULL AND user_id = :user_id
    );
    """

    with engine.connect() as connection:
        result = connection.execute(text(query), {"user_id": data["user_id"]})
        rows = result.mappings().all()
        if not rows:
            return {"message": "You haven't checked out any books"}
        return {"data": list(rows)}


@app.post("/signup")
async def signup(request: Request):
    """Create a new user in the database."""
    data = await request.json()
    try:
        create_user = supabase.auth.sign_up({"email": data["email"], "password": data["password"]})
    except Exception as e:
        return {"message": str(e), "status": 400}

    supabase_service_client.table("users").insert({"supabase_id": create_user.user.id}).execute()
    return {"message": "User created successfully", "status": 200}


@app.post("/logout")
async def logout():
    """Logs out the current user."""
    supabase.auth.sign_out()
    return {"message": "Logged out successfully"}


@app.get("/user")
async def get_user(request: Request):
    """Return the user id of the user whose auth token was provided."""
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token required")

    user = supabase.auth.get_user(auth_token)
    return {"user_id": user.user.id}


@app.post("/auth")
async def post_auth(request: Request):
    """Return a temporary auth token for provided credentials."""
    data = await request.json()
    auth = supabase.auth.sign_in_with_password({"email": data["email"], "password": data["password"]})
    return {"access_token": auth.session.access_token}


@app.put("/book")
async def create_book(request: Request):
    """Create a new book in the database."""
    data = await request.json()
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token required")

    supabase.postgrest.auth(auth_token)
    response = supabase.table("books").upsert({
        "title": data["title"],
        "author": data["author"],
        "isbn": data["isbn"]
    }).execute()

    return response.data


@app.put("/checkout")
async def checkout_book(request: Request):
    """Check out a book."""
    data = await request.json()
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token required")

    supabase.postgrest.auth(auth_token)

    book_check = supabase.table("books").select("*").match({"id": data["book_id"], "is_checked_out": True}).execute()
    if book_check.data:
        return {"message": "This book is not currently available for checkout"}

    due_date = (datetime.now(timezone.utc) + timedelta(days=14)).date().isoformat()
    supabase.table("checkout_logs").upsert({"book_id": data["book_id"], "user_id": data["user_id"]}).execute()
    supabase.table("books").update({"is_checked_out": True, "due_date": due_date}).eq("id", data["book_id"]).execute()

    return {"message": f"Book successfully checked out! Due date: {due_date}"}


@app.put("/return")
async def return_book(request: Request):
    """Return a checked-out book."""
    data = await request.json()
    auth_token = request.headers.get("Authorization")
    current_date = datetime.now(timezone.utc)
    if not auth_token:
        raise HTTPException(status_code=401, detail="Authorization token required")

    supabase.postgrest.auth(auth_token)

    query_check = """
    SELECT * FROM checkout_logs
    WHERE checkin_date IS NULL AND book_id = :book_id AND user_id = :user_id
    """
    query_update = """
    UPDATE checkout_logs
    SET checkin_date = :current_date
    WHERE checkin_date IS NULL AND book_id = :book_id AND user_id = :user_id
    """

    with engine.connect() as connection:
        result = connection.execute(text(query_check), {"book_id": data["book_id"], "user_id": data["user_id"]})
        if result.rowcount == 0:
            return {"message": "This book isn't currently checked out by you"}

        supabase.table("books").update({"is_checked_out": False, "due_date": None}).eq("id", data["book_id"]).execute()
        connection.execute(text(query_update), {
            "book_id": data["book_id"],
            "user_id": data["user_id"],
            "current_date": current_date.strftime('%Y-%m-%d %H:%M:%S %z')
        })
        connection.commit()

    return {"message": "Book successfully returned"}
