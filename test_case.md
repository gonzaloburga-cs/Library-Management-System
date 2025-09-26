# Test Cases Documentation
### Use Case 1: Search Catalog
- **Test Case Name**: Search Catalog by Title (Valid)
- **Description**: Searching valid title returns matching result with availability
- **Use Case**: Search Catalog
- **Inputs**: Example "Great Gatsby"
- **Expected Outputs**: Book title, author, ISBN, availability
- **Pass Criteria**: At least one book is returned with availability
------
- **Test Case Name**: Search Catalog by ISBN (Invalid)
- **Description**: Searching invalid ISBN returns no matches
- **Use Case**: Search Catalog
- **Inputs**: Example "1"
- **Expected Outputs**: "No results found"
- **Pass Criteria**: Message displays and no matching books

### Use Case 2: Checkout Item
- **Test Case Name**: Checkout available book
- **Description**: Verify user can check out available books
- **Use Case**: Checkout Item
- **Inputs**: Book ID
- **Expected Outputs**: Loan created, due date created, book updates to "checked out" or unavaiable
- **Pass Criteria**: Successful checkout and due date assigned
----
- **Test Case Name**: Checkout unavailable book 
- **Description**: Verify user cannot checkout unavailable book
- **Use Case**: Checkout Item
- **Inputs**: Book ID
- **Expected Outputs**: "Book currently not available" / "Make reservation" 
- **Pass Criteria**: Check out is not allowed, loan not created

### Use Case 3: Return Item
- **Test Case Name**: Return borrowed book
- **Description**: Make sure availavilty is updated after book is returned
- **Use Case**: Return Item
- **Inputs**: Book ID
- **Expected Outputs**: "Book successfully returned", loan closes, availability updated 
- **Pass Criteria**: Return goes through and book is available again
----
- **Test Case Name**: Return Item
- **Description**: Return book with incorrect book ID
- **Use Case**: Return Item
- **Inputs**: Book ID
- **Expected Outputs**: "Error: book is not checked out" 
- **Pass Criteria**: Return denied

### Use Case 4: Renew Item
- **Test Case Name**: Book renewal while allowed
- **Description**: Verify user can renew book before due date
- **Use Case**: Renew Item
- **Inputs**: Book ID
- **Expected Outputs**: Booked due date exteneded 
- **Pass Criteria**: Successful renewal and due date exteneded
----
- **Test Case Name**: Overdue book renewal 
- **Description**: Verify user cannot renew book after due date
- **Use Case**: Renew Item 
- **Inputs**: Book ID
- **Expected Outputs**: Renewal not allowed for overdue books
- **Pass Criteria**: Renewal denied

### Use Case 5: Overdue Notification
- **Test Case Name**: Send overdue notification
- **Description**: Make sure notification is send to user once book is overdue
- **Use Case**: Overdue Notification
- **Inputs**: Book ID
- **Expected Outputs**: Email/Notificiation
- **Pass Criteria**: User gets notification
----
- **Test Case Name**: No notification for non overdue books
- **Description**: Make sure notification doesn't send for non overdue books
- **Use Case**: Overdue Notificiation
- **Inputs**: Book ID
- **Expected Outputs**: No email/notification 
- **Pass Criteria**: User doesn't get notificiation

### Use Case 6: Add/remove book
- **Test Case Name**: Add book to catalog
- **Description**: Make sure librarian can add books 
- **Use Case**: Add/remove book
- **Inputs**: Title, author, ISBN
- **Expected Outputs**: Book added to catalog
- **Pass Criteria**: Book successfully added
----
- **Test Case Name**: Remove book from catalog
- **Description**: Make sure librarian can remove books 
- **Use Case**: Add/remove book
- **Inputs**: Title, author, ISBN
- **Expected Outputs**: Book removed from catalog
- **Pass Criteria**: Book successfully removed

### Use Case 7: View current loans
- **Test Case Name**: View checked out books
- **Description**: Make sure users can see their current loaned books
- **Use Case**: View current loans
- **Inputs**: User ID
- **Expected Outputs**: List of checked out books and due dates
- **Pass Criteria**: See books and correct due dates
----
- **Test Case Name**: View loans with no borrowed books
- **Description**: Make sure users don't see books when theres no loaned books
- **Use Case**: View current loans
- **Inputs**: User ID
- **Expected Outputs**: No list  
- **Pass Criteria**: Empty list

### Use Case 8: Reserve Item
- **Test Case Name**: Reserve next checkout for unavailable books
- **Description**: Make sure users and reserve a book once available again
- **Use Case**: Reserve Item
- **Inputs**: User ID, book ID
- **Expected Outputs**: Reservation created, user added to hold queue
- **Pass Criteria**: Successfull reservation
----
- **Test Case Name**: Reserve available book
- **Description**: Make sure users don't reserve available books
- **Use Case**: Reserve Item
- **Inputs**: User ID, book ID
- **Expected Outputs**: Book is available, checkout now
- **Pass Criteria**: Reservation denied
