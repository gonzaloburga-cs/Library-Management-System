# LMS DOCS 

---

### Setup and Running CLI: 
it’s recommended to create a virtual environment for installing the requirements and then running backend/main.py in the venv. 

Note: these instructions may vary slightly depending on OS and directory 

 

- Create a venv in your desired directory: python -m venv .venv 
- backend/.venv/scripts/activate (.venv will be replaced with whatever your virtual environment directory is called. This will activate your venv) 

- pip install -r backend/requirements.txt 

- uvicorn server:app –reload (run this if you need to run the local server but isn’t required for the cli to work as the backend is hosted) Also I cd into the backend before running this otherwise you would probably need to run uvicorn backend.server:app –reload but that was giving me some issues so I think it’s better to just switch to the backend directory first 

- With your venv active run python backend/main.py or python main.py depending on your directory to start the CLI 

 

## For Endpoint testing: 

---

#### Download Postman 

 

- Local URL: http://127.0.0.1:8000 

- Server URL: lms.murtsa.dev (lms for library management system) 

-For testing purposes use the local URL 
( format is url + path i.e. http://127.0.0.1:8000/books to get the list of books if you’re running the server locally or https://lms.murtsa.dev/books for the hosted server)


## Endpoints

---

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

 

 

 
 