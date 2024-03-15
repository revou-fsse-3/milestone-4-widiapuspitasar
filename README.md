# Milestone 4
# Secure and Intuitive Flask API for Banking Application

This project aims to create a secure and intuitive Flask API for a banking application. The API offers features for account management, transactions, security protocols, and user authentication. 

## Key Features

### User Management:
- **POST /users:** Create a new user account.
- **GET /users/id:** Retrieve the profile of the currently authenticated user.
- **PUT /users/id:** Update the profile information of the currently authenticated user.

### Account Management:
- **GET /accounts:** Retrieve a list of all accounts belonging to the currently authenticated user.
- **GET /accounts/:id:** Retrieve details of a specific account by its ID. (Authorization required for account owner)
- **POST /accounts:** Create a new account for the currently authenticated user.
- **PUT /accounts/:id:** Update details of an existing account. (Authorization required for account owner)
- **DELETE /accounts/:id:** Delete an account. (Authorization required for account owner)

### Transaction Management:
- **GET /transactions:** Retrieve a list of all transactions for the currently authenticated user's accounts. (Optional: filter by account ID, date range)
- **GET /transactions/:id:** Retrieve details of a specific transaction by its ID. (Authorization required for related account owner)
- **POST /transactions:** Initiate a new transaction (deposit, withdrawal, or transfer). (Authorization required for related account owner)

## Tables

### Users:
- id (INT, Primary Key): Unique identifier for the user.
- username (VARCHAR(255), Unique): Username for login.
- email (VARCHAR(255), Unique): User's email address.
- password_hash (VARCHAR(255)): Securely hashed user password.
- created_at (DATETIME): Timestamp of user creation.
- updated_at (DATETIME): Timestamp of user information update.

### Accounts:
- id (INT, Primary Key): Unique identifier for the account.
- user_id (INT, Foreign Key references Users.id): User associated with the account.
- account_type (VARCHAR(255)): Type of account (e.g., checking, savings).
- account_number (VARCHAR(255), Unique): Unique account number.
- balance (DECIMAL(10, 2)): Current balance of the account.
- created_at (DATETIME): Timestamp of account creation.
- updated_at (DATETIME): Timestamp of account information update.

### Transactions:
- id (INT, Primary Key): Unique identifier for the transaction.
- from_account_id (INT, Foreign Key references Accounts.id): Account initiating the transaction (optional for transfers).
- to_account_id (INT, Foreign Key references Accounts.id): Account receiving the transaction (optional for deposits).
- amount (DECIMAL(10, 2)): Transaction amount.
- type (VARCHAR(255)): Type of transaction (e.g., deposit, withdrawal, transfer).
- description (VARCHAR(255)): Optional description of the transaction.
- created_at (DATETIME): Timestamp of transaction creation.



