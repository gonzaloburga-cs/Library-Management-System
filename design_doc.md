# Library-Management-System

## Design Document

### 1. High-level functionality
The Library-Management-System (LMS) is a web-based application that allows library staff and users to access library resources, books, borrowing/returning, reservations, and notifications.

- Catalog browsing (title, author, ISBN, subject)  
- Borrowing workflow: checkout, renewals, returns, holds/reservations, overdue notifications  
- Inventory management for librarians: add/remove items  

---

### 2. User Stories

#### Josh (Student)
- As a student, I want to search for the book I need for class and place a hold on it so I can pick it up when it becomes available  

#### Zack (Student)
- As a student, I want to see my current checked-out items and due dates so I can return or renew them on time  

#### Susan (Librarian)
- As a librarian, I want to add new books and update item metadata so the catalog stays accurate  

---

### 3. Use Cases
- **Search Catalog** — Student or staff searches books by title, author, ISBN, or subject; results show availability  
- **Checkout Book** — Student checks out an item and sets the due date  
- **Return Book** — Process item return and update availability  
- **Renew Book** — Student or staff renews a checked-out item (if allowed)  
- **Overdue Notifications** — System sends reminders when items are overdue  
- **Add / Remove Book** — Librarian manages catalog records  
- **View Current Loans** — User checks their borrowed books and due dates  
- **Place Hold / Reserve Item** — User can reserve an item if unavailable

### 3a. Rainy day use cases
- **Checkout Book** — Item is already checkout. System response: "Book is unavailable. Join waitlist?(y/n)"
- **Return Book** — Return failed. System response: "Error in return process. Enter book ID again"
- **Renew Book** - Renewal failed. System response: "Book cannot be renewed because of  waitlist"
- **Add / Remove Book** —  Duplicate or invalid data. System response: "Adding book error. Try again"

---

### 4. System Architecture
The Library-Management-System is a web-based application with three main components:

#### 1. Frontend
- Website used by students and librarians  
- Allows catalog search, borrowing/returning books, and reserving unavailable books
- Communicates with the backend via API calls 

#### 2. Backend
- Handles application logic and communicates with the database  
- Processes returns, reservations, and notifications
- Implements API endpoints consumed by the frontend and Postman 

#### 3. Database
- Stores books, users, loans, and reservations  
- Ensures data is correct and up to date
- SupaBase is used as a backend database for authentication, storage, and live updates

#### 4. External Systems
- Postman: Test client for API verification
- Email service for sending overdue notifications

#### 5. Libraries
- Alembic and SQLalchemy are both used for our database migrations as well as when we need a more advanced database query than that which the supabase connections is capable.
- Supabase provides an easy way to connect to the database and perform simple operations
- Maskpass and Requests are both used on the frontend maskpass to hide the password being typed in and requests is how we call our endpoints from the frontend.
- Psycopg2 is needed when working with postgreSQL databases like ours and allows us to perform operations on the databse.
- FastAPI is a framework used for creating RESTful API's
- PyQT is used on the frontend to create our GUI
- dotenv is used so that we can more easily work with dot files
---

### 5. Data Flow

#### Searching
- User searches for the desired item  
- Frontend calls GET catalog search  
- Backend queries the database and returns results  
- Frontend displays results with availability  

#### Checkout and Return
- User checks out the book  
- Backend verifies availability and creates a Loan record with `due_at`  
- Return updates `Loan.returned_at` and sets book to available  

#### Overdue Notifications
- Background job checks for loans where `due_at < today` AND `returned_at` is NULL  
- Sends overdue notifications via email

---

### 6. Class Definitions

### UML Diagram
![ClassDefinitions](https://github.com/user-attachments/assets/6d653258-ddb3-45f8-910a-b3cc3405cb43)


