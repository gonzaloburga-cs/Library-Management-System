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
- **Checkout Item** — Student checks out an item and sets the due date  
- **Return Item** — Process item return and update availability  
- **Renew Item** — Student or staff renews a checked-out item (if allowed)  
- **Overdue Notifications** — System sends reminders when items are overdue  
- **Add / Remove Book** — Librarian manages catalog records  
- **View Current Loans** — User checks their borrowed books and due dates  
- **Place Hold / Reserve Item** — User can reserve an item if unavailable  

---

### 4. System Architecture
The Library-Management-System is a web-based application with three main components:

#### 1. Frontend
- Website used by students and librarians  
- Allows catalog search, borrowing/returning books, and reserving unavailable books  

#### 2. Backend
- Handles application logic and communicates with the database  
- Processes returns, reservations, and notifications  

#### 3. Database
- Stores books, users, loans, and reservations  
- Ensures data is correct and up to date  

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
