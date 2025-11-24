# Software Requirements Specification (SRS)
*Based on ISO/IEC/IEEE 29148:2018*
---
## 1. Introduction

### 1.1 Purpose

The point of this SRS is to define the requirements of our Library Management System 
(LMS) project. The target audience for this SRS is for developers, 
testers, and stakeholders who are involved in maintaining the LMS.



### 1.2 Scope

The LMS is a web-based application for users to be able to browse, check out, 
renew, and reserve books. It will reduce manual bookkeeping and improve 
accessibility for users and admins.


### 1.3 Definitions, Acronyms, and Abbreviations

     - LMS: Library Management System
     - Admin: User with higher access to add/remove books
     - User: Library account holder who can check out and reserve books
     - UI: User Interface
    

### 1.4 References

     ISO/IEC/IEEE 29148:2018 
     PyQt6 (Front-end stack)
     SupaBase (Database)
     Python 3.12

### 1.5 Overview

This document will provide the detailed requirements of the LMS. Section 2 will go over the product review, section 3 will be the functional and non-functional requirements, section 4 will have supporting materials like diagrams and a glossary.

---
## 2. Overall Description

### 2.1 Product Perspective

The LMS is a web application with an interface for both users and admins. 
It is integrated with a backend database to store records of books and users.

### 2.2 Product Functions

    - Viewing books available in the catalog
    - Add books with title, author, and ISBN
    - Check out books with book ID
    - Return books with book ID
    - Reserving a book if it's currently unavailable(checked out)
    - Sending overdue notifications
    - User login (if you already have an account)
    - User sign up, creating an account to have access to LMS


### 2.3 User Classes and Characteristics

    - Admin - Library staff who can add/remove books (Full access)
    - User - Account holder who can check out and reserve books (Basic access)
    - Guest - Non-member who can only see available books (Limited access)

### 2.4 Operating Environment

    - Web browsers: Chrome, Safari, Edge
    - Operating Systems: Windows, macOS
    - Database: SupaBase
    - Server: Postman
    - Network: Internet

### 2.5 Design and Implementation Constraints

    - Programming language: Python 3
    - GUI: PyQt6
    - Database: SupaBase
    - Must use environment variables to protect API keys 

### 2.6 Assumptions and Dependencies

    - Must have an internet connection
    - The server is consistently available
    - Email notifications are available for overdue alerts
    - User must enter a valid email address for sign-up

---

## 3. Specific Requirements

### 3.1 Functional Requirements

    1. User login/logout
      - User Story: As a user, I want to log in and out of my account for security
    2. User sign up
      - User Story: As a new user, I want to create an account so I can check out books
    3. Admin login
      - User Story: As an admin user, I want to log in so that I can manage the catalog
    4. Add books
      - User Story: As an admin user, I want to add books so that users have a big variety to choose from
    5. Remove books
      - User Story: As an admin user, I want to remove books that are damaged until they are fixed or replaced
    6. See book collection
      - User Story: As a user, I want to see all the books available so that I can choose something I like
    7. See users checked out books
      - User Story: As an admin user, I want to see checked-out books to manage inventory
    8. See the checked out book due date
      - User Story: As a user, I want to see all my checked-out books so I can return them on time
    9. Search books
      - User Story: As a user, I want to search for books by title so I can get them faster
    10. Check out books
      - User Story: As a user, I want to check out books so I can read them on my own time
    11. Check in books
      - User Story: As a user, I want to return books to avoid late fees
    12. Renew checked out books
      - User Story: As a user, I want to renew books to have more time to finish them
    13. Reserve books
      - User Story: As a user, I want to reserve books so that I can check them out once they're available

#### 3.1.1 Acceptance Tests
    - User login/logout
      - Given: Registered user exists
      - When: User enters existing account credentials 
      - Then: User gets logged in and given access to LMS features

    - Check out books
      - Given: Book is available
      - When: User requests to check out
      - Then: Book is marked unavailable, and the due date is assigned

### 3.2 Non-Functional Requirements

    Security: The system covers the user's password during login for safety
    Reliable: The system is responsive on desktop and mobile devices
    Maintainable: The code will allow for future updates and expansion

### 3.3 External Interface Requirements

    Software Interface: Integration with database (SupaBase)
    Communication Interface: Uses HTTPS for secure data transfer
    UI: Uses PyQt6 with buttons, forms, and navigation


### 3.4 Logical Database Requirements

User: (email, password, borrowed books)
Book: (book ID, title, author, ISBN)
Transaction: (book ID, checkout date, return date)


### 3.6 Software System Attributes

    Discuss system qualities like:
    
    - Reliability | System recovers from minor faults
    - Availability | Accessible 24/7 (unless under scheduled maintenance)
    - Security | Protects users' accounts by covering passwords 
    - Maintainability | Good code structure for easy debugging
    - Portability | Compatible with different browsers and devices

### 3.7 Traceability Matrix
- links project requirements to deliverables

| Requirement ID | Requirement Description | Design Element | Test Case ID |
|----------------|------------------------|----------------|--------------|
| FR1 | User login/logout | Login Form UI, Authentication Module | TC1 |
| FR2 | User sign up | Sign-up Form UI, Database User Table | TC2 |
| FR4 | Add books | Admin Dashboard, Database Book Table | TC3 |
| FR9 | Search books | Search UI, Search API Endpoint | TC4 |
| FR10 | Check out books | Book Detail UI, Transaction Module | TC5 |
| FR12 | Renew checked-out books | Transaction Module, User Dashboard | TC6 |
| FR13 | Reserve books | Reservation Module, Book Status Field | TC7 |
| FR15 | Late penalty charge | Transaction Module, Penalty Calculation Function | TC8 |
| NFR1 | Security | Encryption Module, HTTPS Communication | TC9 |


---

## 4. Appendices

### A. Glossary

Section 1.3

## Removed sections
    3.5 Design Constraints: Overlaps with 2.5
    C. Index: Each section is already labeled


