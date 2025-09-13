#!/usr/bin/env python3
from fastapi import FastAPI, Depends, Request

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

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


