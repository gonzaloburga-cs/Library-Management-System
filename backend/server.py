#!/usr/bin/env python3

from fastapi import FastAPI, Depends, Request

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from datetime import datetime, timezone

from dotenv import load_dotenv

from supabase import create_client, Client

import os

load_dotenv()

url = os.getenv("SUPABASE_DATABASE_URL")

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base

# use subabase for almost everything. supabase_service_client is currently only for creating users
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_PUBLIC_KEY"))
supabase_service_client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SECRET_KEY"))


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


# Used to test if the server is running
@app.get("/")
def hello_world():
    return {"message": "Hello World"}


# Return a list of books
@app.get("/books")
def get_books():
    response = (supabase.table("books").select("*").execute())
    return response


# Returns a list of books checked out by the logged-in user
@app.get("/my-books")
async def get_my_books(request: Request):
    data = await request.json()
    auth_token = request.headers["Authorization"]
    supabase.postgrest.auth(auth_token)

    # queries
    my_books = "select id, title, author, isbn from books where id in (select book_id from checkout_logs where checkin_date IS NULL AND user_id=:user_id);"

    with engine.connect() as connection:
        result = connection.execute(text(my_books), {"user_id": data["user_id"]})
        data = {"data": []}
        if result.rowcount == 0:
            response = "You haven't checked out any books"
        else:
            for book in result:
                data["data"].append({"id": book._data[0], "title": book._data[1], "author": book._data[2], "isbn": book._data[3]})
            response = data

    return response


@app.post("/signup")
async def signup(request: Request):
    data = await request.json()

    create_user = supabase.auth.sign_up({"email": data["email"], "password": data["password"]})

    supabase_id = create_user.user.id
    supabase_service_client.table("users").insert({"supabase_id": supabase_id}).execute()

    return "User created successfully"


@app.get("/user")
async def get_user(request: Request):
    auth_token = request.headers["Authorization"]
    user = supabase.auth.get_user(auth_token)
    response = user.user.id

    return response


# Returns a temporary auth token of the user whose credentials were provided
@app.post("/auth")
async def post_auth(request: Request):
    data = await request.json()
    auth = supabase.auth.sign_in_with_password({"email": data["email"], "password": data["password"]})
    session = auth.session
    return session.access_token


# Creates a new book in the database
# Requires an auth token in the header of your request
# todo check for existing isbn and throw in an error or in the future
#  increment quantity (column needs to be added to database)
@app.put("/book")
async def create_book(request: Request):
    data = await request.json()
    auth_token = request.headers["Authorization"]

    supabase.postgrest.auth(auth_token)
    response = (
                supabase.table("books")
                .upsert({"title": data["title"], "author": data["author"], "isbn": data["isbn"]})
                .execute()
    )

    return response


@app.put("/checkout")
async def create_book(request: Request):
    data = await request.json()
    auth_token = request.headers["Authorization"]
    supabase.postgrest.auth(auth_token)

    # check if the book is already checked out
    is_checked_out = supabase.table("books").select("*").match({"id": data["book_id"], "is_checked_out": True}).execute()
    if is_checked_out.data:
        response = "This Book is not currently available for checkout"
    else:
        supabase.table("checkout_logs").upsert({"book_id": data["book_id"], "user_id": data["user_id"]}).execute()
        supabase.table("books").update({"is_checked_out": True}).eq("id", data["book_id"]).execute()
        response = "Book successfully checked out"

    return response


@app.put("/return")
async def create_book(request: Request):
    data = await request.json()
    auth_token = request.headers["Authorization"]
    current_date = datetime.now(timezone.utc)
    supabase.postgrest.auth(auth_token)

    # queries
    is_checked_out = "SELECT * FROM checkout_logs WHERE checkin_date IS NULL AND book_id = :book_id AND user_id = :user_id"
    return_book = "UPDATE checkout_logs SET checkin_date = :current_date where checkin_date IS NULL AND book_id = :book_id AND user_id = :user_id"

    with engine.connect() as connection:
        result = connection.execute(text(is_checked_out), {"book_id": data["book_id"], "user_id": data["user_id"]})
        if result.rowcount == 0:
            response = "This book isn't currently checked out by you"
        else:
            supabase.table("books").update({"is_checked_out": False}).eq("id", data["book_id"]).execute()
            connection.execute(text(return_book), {"book_id": data["book_id"], "user_id": data["user_id"],
                                                   "current_date": current_date.strftime('%Y-%m-%d %H:%M:%S %z')})
            connection.commit()
            response = "Book successfully returned"

    return response

