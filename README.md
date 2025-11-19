# Library-Management-System

This Repo is for team charlie in CS 2450 at UVU.

## Using the GUI

There is an EXE available in the root of the repo. It will install the GUI onto your machine. If you would like to test the python code yourself, keep reading.

Before starting the GUI make a virtual environment in whatever directory your would like with python with the command `python -m venv .venv` and then run `path/to/environment/.venv/scripts/activate` and install the necessary dependancies with `pip install -r frontend/requirements.txt`

### Home Page

The app will open to the home page where you can see all of the books in the database, and their check out status as well. Books cannot be checked out until you have signed in, this can be done by pressing the login button.

<img width="952" height="632" alt="image" src="https://github.com/user-attachments/assets/a0cf82da-1537-4de4-88cb-1c4c3c2096a3" />


### My Books Page

The My Books page shows books you have checked out and allows you to return them. You cannot access this page without signing in, and you will be prompted to do so if you try.

<img width="952" height="632" alt="image" src="https://github.com/user-attachments/assets/08ef687d-7b9e-47e4-acfa-5798b8338da5" />


### Sign up

To sign up, first press the login button, then enter your desired credentials and then click sign up. This will add your user to the database. Then you can sign in by pressing the login button again and entering your credentials and pressing Login. Once this is done you can access the full functionality of the app.

<img width="952" height="632" alt="image" src="https://github.com/user-attachments/assets/921006d7-97c6-4335-bcd9-f531f8c25410" />

<img width="302" height="182" alt="image" src="https://github.com/user-attachments/assets/16b109d2-0e10-4b3e-aea4-4dff609cf295" />



## Setup and Running CLI
it’s recommended to create a virtual environment for installing the requirements and then running backend/main.py in the venv. 

Note: these instructions may vary slightly depending on OS and directory 

- Change to the backend folder: `cd backend`
- Create a virtual environment for the backend of the app (This includes the server and the CLI): `python -m venv .venv`
- Activate the venv: `.venv/scripts/activate` (.venv will be replaced with whatever your virtual environment directory is called.)

- next, install the dependancies for the backend (This includes the dependancies to run the server locally): `pip install -r requirements.txt` 

<img width="1034" height="104" alt="image" src="https://github.com/user-attachments/assets/5f6a046c-f4e0-49a1-898e-605fce448f88" />

- If you want to run the backend server locally run: `uvicorn server:app –reload` The server is hosted, so this is not necessary for regular usage.

- With your venv active, run `python main.py` to start the CLI.

<img width="882" height="28" alt="image" src="https://github.com/user-attachments/assets/324f73e3-7cfc-421a-a930-e0d09526a07f" />

- Main Menu:

<img width="285" height="223" alt="image" src="https://github.com/user-attachments/assets/b4acc376-6bb0-4cb4-b988-cb81ee5d1a35" />

Once you are on the main menu, enter the number for the option that you would like to activate.

## For Endpoint testing

#### Download Postman (For testing purposes only)
 

- Local URL: http://127.0.0.1:8000 

- Server URL: lms.murtsa.dev (lms for library management system) 

-For testing purposes use the local URL 
( format is url + path i.e. http://127.0.0.1:8000/books to get the list of books if you’re running the server locally or https://lms.murtsa.dev/books for the hosted server)


## Endpoints


### / (hello world to test if the server is running) 


-get request 

 ---

### /signup (creates a new user) 



-post request 

-takes an email and password in json format i.e. {"email": "your-email", "password": "your-password"} 

-adds the user to the auth table and user table 

 ---

### /auth (returns an auth token for the specified user) 



-post request 

-include in the body as Json the email and password of the user 

body > raw > JSON > {"email": "your-email", "password": "your-password"} 

 ---

### /user (returns the users id) 



-get request 

-requires auth token 

 ---

### /books (returns the list of books in the database) 



-get request 

-no auth required 

 ---

### /book (add a book to the database) 



-auth required 

-put request 

in postman add a header (key = Authorization, value = your auth token) 

in postman in the body > raw > JSON> {"title": "book title", "author": "book author", "isbn": "isbn #"} 

 ---

### /checkout (checkout a book) 



-put request 

-needs auth token, user_id, and book_id 

-if the book is available adds a row to the checkout_logs table and sets the book to checked out 

 ---

### /return (return a checked out book) 



-put request 

-needs auth token, and book_id 

-looks in the checkout_logs table for that book_id with a null checkin_date 

 

 

 
 
