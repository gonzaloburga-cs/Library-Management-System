# SRS (AI-Revised Version)

*Updated for clarity, completeness, consistency, and alignment with ISO/IEC/IEEE 29148:2018*

## 1. Introduction
### 1.1 Purpose

The purpose of this Software Requirements Specification (SRS) is to define the functional and non-functional requirements for the Library Management System (LMS). This document is intended for developers, testers, project managers, and stakeholders involved in the design, implementation, and maintenance of the LMS.

### 1.2 Scope

The LMS is a web-based application that enables users to browse, borrow, renew, and reserve books. Administrators can manage the catalog, user accounts, and checkout activity. The system reduces manual library operations and improves accessibility through a centralized interface.

### 1.3 Definitions, Acronyms, and Abbreviations
      Term	Definition
    - LMS	Library Management System
    - Admin	Authorized staff member with full system access
    - User	Registered library member with borrowing privileges
    - Guest	Unregistered visitor with limited access
    - UI	User Interface
  
### 1.4 References

    ISO/IEC/IEEE 29148:2018

    Python 3.12

    Supabase (Database)

    PyQt6 (Front-end framework)

### 1.5 Overview

Section 2 provides a system description and context.
Section 3 defines all functional and non-functional requirements.
Section 4 provides additional supporting information, including a glossary and diagrams (if applicable).

## 2. Overall Description
### 2.1 Product Perspective

The LMS is a standalone web application consisting of:

A front-end interface for Admins, Users, and Guests

A backend API layer

A Supabase database for persistent storage

It is integrated with external services such as email notification systems for overdue reminders.

### 2.2 Product Functions

    - Major system capabilities include:

    - Browse and search the catalog

    - User authentication (login, signup)

    - Admin book management (add, remove, update)

    - Checkout and return of books

    - Renew items before due date

    - Reserve items currently checked out

    - Automated overdue notifications

### 2.3 User Classes and Characteristics

    - Admin: Full access; manages catalog and user activity

    - User: Can check out, reserve, and renew books

    - Guest: Can only view catalog; no account or checkout privileges

### 2.4 Operating Environment

    - Browsers: Chrome, Edge, Safari

    - OS: Windows, macOS

    - Database: Supabase

    - Network: Internet connection required

    - Frontend: PyQt6 application wrapper

### 2.5 Design and Implementation Constraints

    - Written in Python 3

    - Must utilize environment variables for API keys

    - Must comply with Supabase schema and API constraints

    - Must follow organizational security policy

### 2.6 Assumptions and Dependencies

    - Users will provide valid email addresses

    - Internet connection is reliable

    - External email service is available for notifications

    - Supabase hosting remains operational
  ---

## 3. Specific Requirements
### 3.1 Functional Requirements

Each requirement includes a description and associated user story.

#### FR1 – User Authentication

    Login and logout

    User Story: As a user, I want to securely access my account.

#### FR2 – User Registration

    Create new accounts

    User Story: As a new user, I want to sign up to borrow books.
    
#### FR3 – Admin Authentication
    
    Admin login with elevated privileges
    
#### FR4 – Catalog Management (Admin)
    
    Add and remove books
    
    User Story: As an admin, I want to maintain the catalog.
    
#### FR5 – View Catalog
    
    Users and guests can browse available books
    
#### FR6 – Search Catalog
    
    Search by title, author, or ISBN
    
#### FR7 – Check Out Books

    User Story: As a user, I want to borrow books and receive a due date.
    
#### FR8 – Return Books
    
    User Story: As a user, I want to return books to avoid penalties.
    
#### FR9 – Renew Books
    
    User Story: As a user, I want more time to finish my books.
    
#### FR10 – Reserve Books
    
    Reserve an unavailable book
    
#### FR11 – Admin View of User Activity
    
    Admins can see checked-out books and due dates
    
#### FR12 – Overdue Notification Service
    
    Automated email reminders

3.1.1 Acceptance Tests

#### AT1 – Login

    Given valid credentials

    When user logs in

    Then the system grants access and loads dashboard

#### AT2 – Checkout

    Given available book

    When user checks it out

    Then system marks it unavailable and assigns a due date

#### 3.2 Non-Functional Requirements

    Security:
    
    - Passwords encrypted in transit and at rest
    
    - Only authorized roles may access restricted features
    
    Reliability:
    
    - 24/7 uptime except scheduled maintenance
    
    - Handles minor failures with graceful recovery
    
    Maintainability:
    
    - Modular Python codebase
    
    - Clear naming conventions and documentation
    
    Performance:
    
    - Catalog search returns results within 2 seconds
    
    - Login response within 1 second
    
    Usability:
    
    - UI must be intuitive for non-technical users

3.3 External Interface Requirements

    Database: Supabase tables for Users, Books, Transactions

    UI: PyQt6 for front-end interactions
    
    Network: HTTPS for secure communication

3.4 Logical Database Requirements

    User: user_id, password hash, borrowed_books
    Book: book_id, title, author, ISBN, status
    Transaction: book_id, user, checkout_date, return_date, due_date

3.6 Software System Attributes

    Availability
    
    Reliability
    
    Security
    
    Maintainability
    
    Portability

### 3.7 Traceability Matrix


| ID | Requirement |	Design Element |	Test Case |
|----------------|------------------------|----------------|--------------|
| FR1 |	Login |	Auth Module |	TC1 |
| FR2	| Sign Up	| User | Table |	TC2 |
| FR4	| Add Books |	Admin Dashboard |	TC3 |
| FR6	| Search	| Search API	| TC4 |
| FR7	| Checkout |	Transaction Module |	TC5 |
| FR9	| Renew	User Dashboard	| TC6 |
| FR10 |	Reserve |	Reservation Module |	TC7 |
| NFR1	| Security	| HTTPS,  Encryption |	TC9 |

---

## 4. Appendices
### A. Glossary

Contains terminology defined in Section 1.3.


# Critique
*A critique of the AI revised SRS.md*

## 1. Improvments Made

### 1.1 Structure & Clarity
The AI restructured the document to match IEEE conventions more closely. In some 
cases it made sections more clear, although I had to make some alterations to the
display to keep the design consistent and pretty across the whole document. After
these adjustments, I find the document more readable than the original.

### 1.2 Expanding Requirement Details
The AI rewrote some of the functional requirements with definitions that were more
descriptive. We had some requirements that were somewhat vague, or required expansion,
which the AI accomplished. Although these changes were made without clarifying our 
intention,the added clarity would help keep our team all on the same page. 

### 1.3 Additional Non-Functional Requirements
The AI added some additional non-functional requirements to our SRS. Again, these
changes were made without checking if these requirements were accurate to our goals,
so reading over the document is important to confirm or modify changes made. These
changes do make our program more measurable and also give some suggestions on goals
for us to pursue. This could improve our program and also make it more testable.

### 1.4 Terminology Alterations
The AI changed certain terminology that we used to be more consistent (eg. "Checkout" ->
"Checkout"). It made terms more consistent across the document as well.

## 2. Problems With the AI Revision

### 3.1 Added Features
The AI added certain features that weren't included in our original document.
For example:

    Performance metrics
    Backend API layer
    Password encryption details

It expanded the scope without any prompting to do so. These additions could be beneficial,
but it may lead to confusion and inconsistency between our existing program and our SRS,
or could cause confusion on what our goals are for the project.

### 3.2 Removed and Altered Content
There were multiple instances of the AI removing content or generalizing details in our
document. Some examples are:

    Acceptance tests were shortened
    Traceability matrix items removed, and elements shortened
    System attributes shortened
    
### 3.3 Attribute Name Changing
The AI changed some of the database attribute names (eg. "email" -> "user_id"), which could
cause confusion.

## 4. Summary
The AI revision could be very useful, although it's important to revise any changes made 
carefully. Comparing it to the original document could be beneficial to ensure that nothing
is missing and to make sure that naming conventions are consistent with what you want the 
team to use. It could definitely help make the SRS more readable with a structure that is
more clear. It was moderately accurate, very clear, and somewhat consistent with our original
scope. For SRS revision, it could be a helpful tool in revising a draft, but human revision 
is definitely necessary.
