# Library-Management-System — Design Document (Revised)

## 1. High-Level Functionality
The Library-Management-System (LMS) is a web-based application allowing students and librarians to access, manage, and track library resources.

- **Catalog browsing:** Search by title, author, ISBN, or subject.  
- **Borrowing workflow:** Checkout, renewals, returns.  
- **Inventory management:** Add/remove books and manage metadata.  

---

## 2. User Stories

#### Josh (Student)
- I want to search for books I need and place a hold so I can pick them up when available.  

#### Zack (Student)
- I want to see my currently checked-out books and due dates to manage timely returns.  

#### Susan (Librarian)
- I want to add new books and update item metadata to keep the catalog accurate.  

---

## 3. Use Cases

| Use Case | Description | Rainy Day Scenario |
|----------|-------------|------------------|
| Search Catalog | Search books by title, author, ISBN, or subject; display availability | No results found → “No results found” |
| Checkout Book | Student checks out an item and sets due date | Already checked out → “Book unavailable. Join waitlist?” |
| Return Book | Process book return and update availability | Book not checked out → “This book isn’t currently checked out by you” |
| Renew Book | Renew a checked-out book | Renewal blocked due to waitlist → “Book cannot be renewed” |
| Overdue Notifications | Send reminders for overdue books | Failed email → Log error for manual follow-up |
| Add/Remove Book | Librarian manages catalog records | Duplicate/invalid data → “Adding book error. Try again” |
| View Current Loans | User checks borrowed books and due dates | Backend query fails → “Error retrieving loans” |
| Place Hold/Reserve | Reserve unavailable items | Invalid item ID → “Cannot reserve book” |

---

## 4. System Architecture

The LMS has four main components:

### 4.1 Frontend
- **Purpose:** GUI for students and librarians.  
- **Technology:** PyQt6  
- **Functionality:** Search catalog, checkout/return, view loans, place holds.  
- **Communication:** REST API calls to backend.  

### 4.2 Backend
- **Purpose:** Application logic, database interaction, API endpoint management.  
- **Technology:** FastAPI, Supabase, SQLAlchemy  
- **Functionality:** Handle login/signup, CRUD operations for books and users, checkout/return logic, overdue notifications.  
- **Endpoints:**  
  - `GET /books` — list all books  
  - `POST /my-books` — list user’s checked-out books  
  - `POST /signup` — create user  
  - `POST /auth` — login and return auth token  
  - `PUT /book` — add or update book  
  - `PUT /checkout` — checkout book  
  - `PUT /return` — return book  
  - `GET /user` — get user info by token  

### 4.3 Database
- **Purpose:** Store books, users, checkout logs, reservations.  
- **Technology:** Supabase (PostgreSQL backend), optionally SQLAlchemy models for complex queries.  
- **Tables:** `books`, `users`, `checkout_logs`, `reservations`  

### 4.4 External Systems
- Postman — API testing  
- Email service — sending overdue notifications  

### 4.5 Libraries & Dependencies
| Library | Purpose |
|---------|---------|
| PyQt6 | Frontend GUI creation |
| FastAPI | Backend API framework |
| Supabase | Database backend + auth |
| SQLAlchemy | Complex queries and database session management |
| Alembic | Database migrations |
| Requests | API calls from frontend scripts |
| Maskpass | Hiding password input in console |
| Psycopg2 | PostgreSQL database operations |
| Dotenv | Load environment variables from `.env` files |

---

## 5. Data Flow

### 5.1 Searching
1. User enters search query in GUI.  
2. Frontend calls `GET /books?query=<query>` API endpoint.  
3. Backend queries Supabase database.  
4. Backend returns JSON with matching results.  
5. Frontend displays results with availability.

### 5.2 Checkout
1. User selects a book to checkout.  
2. Frontend calls `PUT /checkout` with auth token and book ID.  
3. Backend verifies availability.  
4. Backend inserts a `checkout_log` entry and updates book status.  
5. Backend returns due date.  

### 5.3 Return
1. User selects book to return.  
2. Frontend calls `PUT /return` with auth token and book ID.  
3. Backend updates `checkout_log` with return date and updates book availability.  

### 5.4 Overdue Notifications
- Background job queries `checkout_logs` where `due_at < today` and `returned_at` is NULL.  
- Sends reminder emails to users.  

---

## 6. Packages & User-Defined Classes

### 6.1 Frontend (`frontend/`)
- **MainWindow** — Root GUI window; manages navigation and main views.  
- **LoginDialog** — Handles login/signup interface and authentication.  

### 6.2 Backend (`backend/`)
- **No full backend classes yet** — functionality is implemented as route functions using FastAPI and Supabase.  
- **Potential future classes:**  
  - `User` — encapsulate user info and auth token management.  
  - `Book` — encapsulate book details, status, and metadata.  
  - `CheckoutLog` — manage checkout and return records.

---

## 7. UML Diagram

**Legend:**  
- Green rectangles: Frontend classes  
- Blue rectangles: Backend (future class concepts)  
- Yellow rectangles: Database tables  

![ClassDefinitions](https://github.com/user-attachments/assets/6d653258-ddb3-45f8-910a-b3cc3405cb43)

---

### Notes
- This revised design explicitly includes packages, libraries, frontend/backend distinctions, and future backend class suggestions.  
- API endpoints are now tied directly to data flow for better implementation guidance.  
- Class definitions reflect current implementation plus potential expansions.



# Critique
A critique of this AI-revised document.

##1. Improvements

### 1.1 Structure & Clarity
Some sections were moved or further separated, making the document easier to understand. There were some revisions needed to ensure
consistency with other documents. Turning the use cases, descriptions, and rainy-day use cases was a nice touch. 

### 1.2 Added Details
There were details added to multiple sections in the document. Some examples:
- In section 4.2 it added descriptions of the endpoints that we use.
- In section 4.5 it also added a table of libraries and dependencies.

These add some clarity to the project.

### 1.3 Terminology
The AI changed some of the terminology we used to be more consistent throughout the doc.

--- 

## 2. Problems With the Revised Doc

### 2.1 Added Features
There were some features that the AI took the liberty of adding without any prompting to do so. Examples:
- Backend classes that do not exist
- A legend for colored boxes in our UML diagram, which we did not use.
These additions could be valuable improvements to make to our document, but could also be confusing or change the scope of our
project.

### 2.2 Removed Sections
- The use case flow chart in section 3 was removed.

This reduces context and takes away a nice visual element used to enhance a reader's understanding.

## 3. Summary
This AI-revised document does have a clearer structure and is easier to read. The use of tables could be very helpful to see the 
connections between different aspects of the document (eg. use cases & rainy-day cases). There are some aspects changed or added, 
which could be interpreted as useful suggestions; however, caution is necessary to ensure that these changes aren't accidentally 
blindly accepted, which could lead to confusion down the road.

There were some changes made that weren't ideal, such as removing the flow chart or adding a legend for our UML diagram that didn't 
make sense. A comparison of the document before and after AI-revision is a good idea to keep components you like from each. This 
document could be a great draft to creating a more polished version of the design document.

