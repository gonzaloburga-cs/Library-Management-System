#this is a place-holder file

import sys
import os
import pytest
from fastapi.testclient import TestClient
from backend.server import app
from unittest.mock import patch, MagicMock, mock_open #doesn't touch real files
import backend.main as cli


client = TestClient(app)

#interaction with server
def test_hello_world_server():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_get_books_server():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "data" in response.json()



#Isolated tests for CLI functions (not interacting with server)
#These use "Mock Testing"

def test_print_menu(capsys):
    if "token" in globals():
        del cli.token        #logged out state

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



#patch decorators are applied bottom to top

#logged in tests

@patch("builtins.open", new_callable=mock_open, read_data="fake_token") #mock open to simulate reading a token from file
@patch("backend.main.requests.get") #mock requests.get to simulate server response
@patch("os.remove") #mock os.remove so no files are deleted during testing
def test_is_logged_in_no_token_file(mock_remove, mock_get, mock_file):
    mock_get.return_value.status_code = 401  #simulate invalid/expired token response from server
    assert cli.is_logged_in() == False
    mock_remove.assert_called_once_with("token.txt")
    assert not "token" in globals() #token should be deleted


@patch("builtins.open", new_callable=mock_open, read_data="fake_token") #mock open to simulate reading a token from file
@patch("backend.main.requests.get") #mock requests.get to simulate server response
def test_is_logged_in_success(mock_get, mock_file, capsys):
    mock_get.return_value.status_code = 200  #simulate valid token response from server
    assert cli.is_logged_in() == True
    captured = capsys.readouterr()
    output = captured.out
    assert "Logged in using saved token." in output
    del cli.token  # reset token for later tests




#logout

@patch("backend.main.server.supabase.auth.sign_out")
def test_logout(mock_sign_out):
    cli.token = "fake_token"
    cli.logout()
    mock_sign_out.assert_called_once()
    assert not "token" in globals() #token should be deleted



#login tests

@patch("builtins.input", side_effect=["rootbeerlover@yahoo.com"]) #mock input for email
@patch("backend.main.maskpass.askpass", return_value="Barqs0nT0p!")
@patch("backend.main.requests.get")
@patch("backend.main.requests.post")
def test_login_success(mock_post, mock_get, mock_pass, mock_input, tmp_path):

    '''Simulates server returning valid token and session'''

    post_response = MagicMock()
    post_response.status_code = 200
    post_response.text = "fake_token"
    mock_post.return_value = post_response

    get_response = MagicMock()
    get_response.status_code = 200
    mock_get.return_value = get_response


    with patch("builtins.open", mock_open()) as mock_file:
        cli.login()

    mock_file.assert_called_with("token.txt", "r")



@patch("builtins.input", side_effect=["bugjelly@uvu.edu", "n"]) #mock input for email; n for retry
@patch("backend.main.maskpass.askpass", return_value="bugjam")
@patch("backend.main.requests.post")
def test_login_failure_unauthorized(mock_post, mock_pass, mock_input, capsys, tmp_path):
    token_file = tmp_path / "token.txt"
    cli.token_file_path = str(token_file)
    if token_file.exists():
        token_file.unlink()

    post_response = MagicMock()
    post_response.status_code = 401        #triggers !=200 block in login()
    post_response.reason = "Unauthorized"
    post_response.text = ""
    mock_post.return_value = post_response

    cli.login()

    captured = capsys.readouterr()
    output = captured.out
    assert "Login failed. Status code 401 for reason Unauthorized." in output
    assert "Please check your credentials and try again." in output

@patch("builtins.input", side_effect=["milesdavis@gmail.com", "n"]) #mock input for email; n for retry
@patch("backend.main.maskpass.askpass", return_value="ihatetrumpets")
@patch("backend.main.requests.post")
@patch("backend.main.requests.get")
def test_login_failure_empty_token(mock_get, mock_post, mock_pass, mock_input, capsys, tmp_path):
    token_file = tmp_path / "token.txt"
    cli.token_file_path = str(token_file)
    if token_file.exists():
        token_file.unlink()

    post_response = MagicMock()
    post_response.status_code = 200
    post_response.text = ""  # Simulate empty token response
    mock_post.return_value = post_response

    cli.login()

    captured = capsys.readouterr()
    output = captured.out
    assert "Login failed. Invalid credentials." in output




@patch("builtins.input", side_effect=["jeffbezos@amazon.com"])
@patch("backend.main.maskpass.askpass", return_value="Iamrich")
@patch("backend.main.requests.post")
def test_signup_success(mock_post, mock_pass, mock_input, capsys):
    mock_post.return_value.status_code = 200
    cli.signup()
    captured = capsys.readouterr()
    output = captured.out
    assert "User Created Successfully!" in output


@patch("builtins.input", side_effect=["jeffbezos@amazon.com"])
@patch("backend.main.maskpass.askpass", return_value="Iamrich")
@patch("backend.main.requests.post")
def test_signup_failure(mock_post, mock_pass, mock_input, capsys):
    mock_post.return_value.status_code = 500
    cli.signup()
    captured = capsys.readouterr()
    output = captured.out
    assert "Failed to create user" in output


#get_books
@patch('backend.main.requests.get')
def test_get_books(mock_get, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "id": 1,
                "created_at": "2025-09-26T11:00:00",
                "updated_at": "2025-09-26T11:00:00",
                "title": "Book 1",
                "author": "Frank Herbert",
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
    captured = capsys.readouterr()
    output = captured.out
    assert "Book 1" in output
    assert "Book 2" in output
    assert "2" in output
    assert "1" in output
    assert "Author" in output
    assert "ISBN" in output
    assert "ID" in output
    assert "111-111" in output
    assert "Frank Herbert" in output


@patch('backend.main.requests.get')
def test_get_books_empty(mock_get, capsys):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": []}
    mock_get.return_value = mock_response
    books = cli.get_books()
    captured = capsys.readouterr()
    output = captured.out
    assert books == None



#add_book


@patch("builtins.input", side_effect=["Atlas Shrugged", "Ayn Rand", "123-456"]) #input for the 3 input calls
@patch("backend.main.requests.put") #requests.put is now the first parameter in test (mock_put)
def test_add_book(mock_put, mock_input, capsys):
    cli.token = "fake_token" #simulate being logged in
    mock_put.return_value.status_code = 200
    cli.add_book()
    captured = capsys.readouterr()
    output = captured.out
    assert "Book added successfully!" in output
    mock_put.assert_called_once()

    del cli.token  # reset token for later tests


@patch("builtins.input", side_effect=["Atlas Shrugged", "Ayn Rand", "123-456"]) #input for the 3 input calls
@patch("backend.main.requests.put")
def test_add_book_500(mock_put, mock_input, capsys):
    cli.token = "fake_token"
    mock_put.return_value.status_code = 500
    cli.add_book()
    captured = capsys.readouterr()
    output = captured.out
    assert "Failed to add book. Status code: " in output
    mock_put.assert_called_once()
    del cli.token







#checkout_book
@patch("backend.main.get_books")
@patch("builtins.input", side_effect=["1"]) #input for the 1 input call
@patch("backend.main.requests.get")
@patch("backend.main.requests.put")
def test_checkout_success(mock_put, mock_get, mock_input, mock_get_books, capsys):
    cli.token = "fake_token"
    mock_get.return_value.status_code = 200    #simulates successful and current session
    mock_put.return_value.status_code = 200    #simulates successful checkout
    cli.checkout_book()
    captured = capsys.readouterr()
    output = captured.out
    assert "Book with ID 1 checked out successfully!" in output
    mock_get_books.assert_called_once()
    del cli.token


@patch("backend.main.get_books")
@patch("builtins.input", side_effect=["1"]) #input for the 1 input call
@patch("backend.main.requests.get")
@patch("backend.main.requests.put")
def test_checkout_success(mock_put, mock_get, mock_input, mock_get_books, capsys):
    cli.token = "fake_token"
    mock_get.return_value.status_code = 401    #simulates expired session    #simulates successful checkout
    cli.checkout_book()
    captured = capsys.readouterr()
    output = captured.out
    assert "Session expired sign in again to checkout a book" in output
    mock_get_books.assert_called_once()
    del cli.token

@patch("backend.main.get_books")
@patch("builtins.input", side_effect=["1"]) #book id
@patch("backend.main.requests.get")
@patch("backend.main.requests.put")
def test_checkout_already_checked_out(mock_put, mock_get, mock_input, mock_get_books, capsys):
    cli.token = "fake_token"
    mock_get.return_value.status_code = 200    #simulates valid session
    mock_put.return_value.status_code = 400    #simulates book already checked out

    cli.checkout_book()

    captured = capsys.readouterr()
    output = captured.out

    assert "Book with ID 1 has already been checked out by another user" in output
    mock_get_books.assert_called_once()
    del cli.token

#return_book
@patch("backend.main.get_books")
@patch("builtins.input", side_effect=["1"]) #input for the 1 input
@patch("backend.main.requests.get")
@patch("backend.main.requests.put")
def test_return_book_success(mock_put, mock_get, mock_input, mock_get_books, capsys):
    cli.token = "fake_token"
    mock_get.return_value.status_code = 200    #simulates valid session
    mock_put.return_value.status_code = 200    #simulates successful return

    cli.return_book()
    captured = capsys.readouterr()
    output = captured.out
    assert "Book with ID 1 was returned successfully!" in output
    mock_get_books.assert_called_once()
    del cli.token



@patch("backend.main.get_books")
@patch("builtins.input", side_effect=["1"]) #input for the 1 input
@patch("backend.main.requests.get")
@patch("backend.main.requests.put")
def test_return_book_not_checked_out(mock_put, mock_get, mock_input, mock_get_books, capsys):
    cli.token = "fake_token"
    mock_get.return_value.status_code = 200    #simulates valid session
    mock_put.return_value.status_code = 500    #simulates book not checked out by user

    cli.return_book()
    captured = capsys.readouterr()
    output = captured.out
    assert "Book with ID 1 hasn't been checked out by you" in output
    mock_get_books.assert_called_once()
    del cli.token


#clear_screen

@patch("backend.main.os.system")
def test_clear_screen(mock_os):
    cli.clear_screen()
    if sys.platform == "win32":
        mock_os.assert_called_once_with("cls")
    else:
        mock_os.assert_called_once_with("clear")

