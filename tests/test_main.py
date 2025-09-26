#this is a place-holder file

import sys
import os
import pytest
from fastapi.testclient import TestClient
from backend.server import app
from unittest.mock import patch, MagicMock
import backend.main as cli


client = TestClient(app)

def test_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_get_books_server():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "data" in response.json()


#print_menu

def test_print_menu(capsys):
    if "token" in globals():
        del cli.token

    cli.print_menu()
    captured = capsys.readouterr()
    output = captured.out

    assert "Library Management System Menu" in output
    assert "0. Show Menu" in output
    assert "1. View Books" in output
    assert "2. Add Book" in output
    assert "3. Checkout Book" in output
    assert "4. Return Book" in output
    assert "5. Login" in output
    assert "6. Exit" in output


#hello_world

#login

#get_books
@patch('backend.main.requests.get')
def test_get_books(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "id": 1,
                "created_at": "2025-09-26T11:00:00",
                "updated_at": "2025-09-26T11:00:00",
                "title": "Book 1",
                "author": "Author 1",
                "isbn": "111-111",
                "is_checked_out": False
            },
            {
                "id": 2,
                "created_at": "2025-09-26T11:05:00",
                "updated_at": "2025-09-26T11:05:00",
                "title": "Book 2",
                "author": "Author 2",
                "isbn": "222-222",
                "is_checked_out": True
            }
        ]
    }
    mock_get.return_value = mock_response

    books = cli.get_books()


#add_book

#checkout_book

#return_book

#clear_screen

#main?