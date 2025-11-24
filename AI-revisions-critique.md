# backend/Server.py      

## 1. Improvements Made

### 1.1 Readability
Through a few changes, the AI was able to improve the clarity of the code. Some changes were also supposedly aligned better with the
"Best Practices" of libraries are used. Specifically, replacing `_data` with `result.mappings()`. It also added some docstrings for 
functions without. Some lines (such as line 65 of the original, which contained a SQL query) were restructured to be typed across 
multiple lines, making it easier to read. Having code that is more readable also increases the maintainability of that code.

### 1.2 Error Handling
The AI expanded error-handling in some functions. For example, in "/my-books", the AI added a branch where if the server returns a 401 
status code, a readable error is thrown. It may not be the most user-friendly, but it makes the code more traceable. 

### 1.3 JSON methods
The AI made some changes (like in /book) to the way we accessed certain data. For example, we had this line `auth_token = request.headers["Authorization"]`
which the AI replaced with `auth_token = request.headers.get("Authorization")`. The functionality stays the same, but using .get() is
a safer method to avoid errors or handle them more gracefully by returning None.

## 2. Issues With the Revision

### 2.1 Format changes
The AI changed the format of the returns made by the endpoints. While this could be useful, we already have measures in place to accept
the responses as they are. Making these alterations this late in the project is unnecessary.

### 2.2 Removed Some Functionality
The AI left out some parts of the code unexpectedly. In "/my-books" and "/checkout" it omitted the "due_date" column from the responses.



## Measurable Results
--------------------------

**Reduction in Code Errors**  
- By replacing internal `_data` access with `result.mappings()` and adding proper authorization checks, the likelihood of runtime errors was reduced. 
- Student self-reported improvement: **0% fewer errors** during testing and API calls. Theoretically, the code is more error-resistant with future changes.

**Increase in Code Quality**  
- Improved readability and cleaner query handling if implemented. 
- Docstrings and comments were clarified to make the code easier to maintain and extend.  
- Student self-reported improvement: **~10% improvement** in code clarity and maintainability.

**Improved Documentation Quality & Completeness**  
- Added one additional docstring for the get_db_session() function. 
- Student self-reported improvement: **~10% improvement** in documentation quality. 

 ---



# frontend/main.py

## 1. Improvements Made

### 1.1 Readability
There were many structural changes made by the AI. For example, a lot of what we had in __init__(), the AI moved into load_colors(), making
things more modular and easier to digest. It also used some bigger organizational comments such as:

    # ------------------------------
    # UI Setup Methods
    # ------------------------------

These are pretty helpful when reading over the setup of the main window. 

### 1.2 Better Documentation
Some of the docstrings were shortened to be more concise. The message remained the same for most of these, in some cases, additional 
detail was added for increased clarity.

### 1.3 Improved functions
Some functions were reworked to do the same thing more efficiently. An example of this is the changed_search() function. The AI-revised
version was cleaner and more compact. It also returned immediately if the search box was empty, rather than searching anyway.




## 2. Issues With the Revision

### 2.1 Over-Abstraction
The AI-revision split up the __init__() function into multiple smaller functions. This could be good, but it could also be a little confusing
and unnecessary.



## Measurable Results
--------------------------

**Reduction in Code Errors**  
- Not much was done to reduce code errors; rather, the changes made were bigger improvements to readability, efficiency, and maintainability.
- Student self-reported improvement: **0% fewer errors** during testing and API calls. Theoretically, the code is more error-resistant with future changes.

**Increase in Code Quality**  
- Functions are more modular, it's easier to tell what each function is doing
- Some functions were reworked to be more efficient.
- Student self-reported improvement: **~20% improvement** in code clarity and maintainability.

**Improved Documentation Quality & Completeness**  
- Docstrings were made more concise, and sometimes had more detail.
- Student self-reported improvement: **~10% improvement** in documentation quality. 

 ---

# frontend/login_dialog.py

## 1. Improvements made

### 1.1 Readability
The AI restructured the login_dialog by breaking it into sections, using the same labels as before:

    # ------------------------------
    # UI CONSTRUCTION
    # ------------------------------

It also created helper functions like `_build_ui()` or `_styled_button()`. This modularity helps make the code easier to understand.

### 1.2 Better Documentation
Certain docstrings were expanded upon to provide a further explanation of their purpose. For example, the responsibilities of the LoginDialog class
were added in the docstring.

### 1.3 More Graceful Error-Handling
In some functions such as `login()`, warning boxes were added to more gracefully handle any errors, such as `f"Network Error, Failed to reach server:\n{e}"`



## Measurable Results
--------------------------

**Reduction in Code Errors**  
- There weren't any known bugs that were fixed here, however, the code should be easier to navigate in case of future issues.
- Student self-reported improvement: **0% fewer errors**. With expanded error handling, it should be easier to debug with future issues.

**Increase in Code Quality**  
- The increased modularity in the UI setup makes it easier to understand.
- Button and input styling is more reusable.
- Some functions were reworked to be more efficient.
- Student self-reported improvement: **~25% improvement** in code clarity and maintainability.

**Improved Documentation Quality & Completeness**  
- Docstrings were expanded upon. They're more descriptive and clearly outline the purpose of each function
- Student self-reported improvement: **~20% improvement** in documentation quality. 

 ---
