CREATE DATABASE `milestones4` ;

USE milestones4

-- Users table
CREATE TABLE user (
    id INT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    email VARCHAR(255) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- Accounts table
CREATE TABLE accounts (
    id INT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    account_type VARCHAR(255),
    account_number VARCHAR(255) UNIQUE,
    balance DECIMAL(10, 2),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
);

-- Transactions table
CREATE TABLE transactions (
    id INT PRIMARY KEY,
    from_account_id INT,
    FOREIGN KEY (from_account_id) REFERENCES accounts(id),
    to_account_id INT,
    FOREIGN KEY (to_account_id) REFERENCES accounts(id),
    amount DECIMAL(10, 2),
    type VARCHAR(255),
    description VARCHAR(255),
    created_at TIMESTAMP NOT NULL
);