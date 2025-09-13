#!/usr/bin/env python3
from fastapi import FastAPI, Depends, Request

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from dotenv import load_dotenv

import os

load_dotenv()

url = os.getenv("SUPABASE_DATABASE_URL")

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/")
def hello_world():
    return {"message": "Hello World"}


# Return a list of books
@app.get("/books")
def get_books(db: SessionLocal = Depends(get_db_session)):
    limit = 10

    # get books from database
    rows = db.execute(text("SELECT * FROM books"))
    # return the list of books
    response = rows.mappings().all()
    return response


# Creates a new book in the database
# todo check for existing isbn and throw in an error or in the future increment quantity (column needs to be added to database)
@app.put("/book")
async def create_book(request: Request, db: SessionLocal = Depends(get_db_session)):
    data = await request.json()
    result = db.execute(text("INSERT INTO books (title, author, isbn) VALUES (:title, :author, :isbn) RETURNING *"),
                      {"title": data["title"], "author": data["author"], "isbn": data["isbn"]})
    db.commit()
    response = result.mappings().one()
    return dict(response)


