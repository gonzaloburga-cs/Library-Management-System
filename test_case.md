# Test Cases Documentation

### Use Case 1: View Books

* **Test Case Name**: View checked out books
* **Description**: Make sure users can see their current loaned books
* **Use Case**: View current loans
* **Inputs**: 1
* **Expected Outputs**: List of checked out books
* **Pass Criteria**: See list of books

---

* **Test Case Name**: View loans with no borrowed books
* **Description**: Make sure users don't see books when there are no loaned books
* **Use Case**: View current loans
* **Inputs**: 1
* **Expected Outputs**: No list
* **Pass Criteria**: Empty list

---

### Use Case 2: Add Book

* **Test Case Name**: Add book to catalog
* **Description**: Make sure users can add books
* **Use Case**: Add book
* **Inputs**: 2, Title, Author, ISBN
* **Expected Outputs**: Book added to catalog
* **Pass Criteria**: Book successfully added

---

* **Test Case Name**: Add invalid book to catalog
* **Description**: Make sure user cannot add invalid books
* **Use Case**: Add book
* **Inputs**: 2, Title, Author, ISBN
* **Expected Outputs**: Book not added to catalog
* **Pass Criteria**: Book addition denied

---

### Use Case 3: Checkout Book

* **Test Case Name**: Checkout available book
* **Description**: Verify user can check out available books
* **Use Case**: Checkout Book
* **Inputs**: Book ID
* **Expected Outputs**: Loan created, due date assigned, book marked unavailable
* **Pass Criteria**: Successful checkout

---

* **Test Case Name**: Checkout unavailable book
* **Description**: Verify user cannot check out unavailable book
* **Use Case**: Checkout Item
* **Inputs**: Book ID
* **Expected Outputs**: "Book currently not available"
* **Pass Criteria**: Checkout denied, loan not created

---

### Use Case 4: Return Item

* **Test Case Name**: Return borrowed book
* **Description**: Make sure availability is updated after book is returned
* **Use Case**: Return Item
* **Inputs**: Book ID
* **Expected Outputs**: "Book successfully returned", loan closes, availability updated
* **Pass Criteria**: Return goes through and book is available again

---

* **Test Case Name**: Return invalid book
* **Description**: Return book with incorrect book ID
* **Use Case**: Return Item
* **Inputs**: Book ID
* **Expected Outputs**: "Error: book is not checked out"
* **Pass Criteria**: Return denied

---

### Use Case 5: Login

* **Test Case Name**: Login with authentication token
* **Description**: Login with authentication token created in sign-up
* **Use Case**: Login
* **Inputs**: Email and Password
* **Expected Outputs**: Login successful
* **Pass Criteria**: Login reads user from database

---

* **Test Case Name**: Login without existing user
* **Description**: Make sure users cannot log in without an existing user
* **Use Case**: Login
* **Inputs**: Email and Password
* **Expected Outputs**: "Login failed, user not found"
* **Pass Criteria**: User cannot access functions without signing in

---

### Use Case 6: Exit

* **Test Case Name**: Exit LMS menu
* **Description**: Quit the LMS menu once done
* **Use Case**: Exit
* **Inputs**: 6
* **Expected Outputs**: Goodbye
* **Pass Criteria**: Program quits successfully

---

* **Test Case Name**: Exit LMS menu
* **Description**: Not quitting program unless 6 is chosen
* **Use Case**: Exit
* **Inputs**: Not 6
* **Expected Outputs**: None
* **Pass Criteria**: Program continues to run successfully

---

### Use Case 7: Sign Up

* **Test Case Name**: User sign up
* **Description**: User needs to create an account before being able to check out, return, or add books
* **Use Case**: Sign up
* **Inputs**: 7, Email, Password
* **Expected Outputs**: Email and Password saved
* **Pass Criteria**: User credentials saved and authentication token created

---

* **Test Case Name**: No login without user sign up
* **Description**: Make sure users sign up before using LMS
* **Use Case**: Sign up
* **Inputs**: 7, Email, Password
* **Expected Outputs**: Cannot create authentication token
* **Pass Criteria**: User login credentials aren't saved
