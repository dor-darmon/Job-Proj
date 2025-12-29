# Assignment 3: SQL Injection Attack & Mitigation

## Overview
This project is a Web Application developed using **Python (Flask)** and **SQLite**.
It serves as a simulation to demonstrate:
1.  **Vulnerability:** How an attacker can bypass authentication using SQL Injection.
2.  **Mitigation:** How to secure the code using Parameterized Queries.
3.  **Persistence:** Upon a successful attack, the malicious payload is logged into the database for demonstration.

## Prerequisites
 Python 3.x
 Flask Library (`pip install flask`)

## Installation & Execution
1.  Navigate to the project folder via terminal/cmd.
2.  Run the application:
    ```bash
    python app.py
    ```
3.  Open your browser and navigate to: `http://127.0.0.1:5001`

---

## Usage Guide

### Scenario 1: The Vulnerable Login (Attack)
This mode simulates a legacy system that uses unsafe string concatenation.

 **Goal:** Log in as `admin` without knowing the password.
 **Username:** `admin`
 **Password (Attack Payload):** `' OR '1'='1`
 **Process:**
    1.  The system injects the input directly into the SQL query string.
    2.  The database interprets `' OR '1'='1` as a logical **TRUE** statement.
 **Result:**
     Login Successful.
     **New Feature:** The system saves the attack payload (`' OR '1'='1`) into the `users` table as a new entry.
     The updated user table is displayed on the screen to prove the data insertion.

### Scenario 2: The Secure Login (Defense)
This mode implements security best practices to neutralize the attack.

 **Goal:** Attempt the same attack and observe the failure.
 **Username:** `admin`
 **Password:** `' OR '1'='1`
 **Process:**
    1.  The system uses **Parameterized Queries** (Prepared Statements).
    2.  The database engine treats the input strictly as *data* (a literal string), not as executable code.
 **Result:**
     Login Failed.
     The system looks for a user whose actual password is the string literal `"' OR '1'='1"`, which does not exist.

---

## Technical Explanation (Code Level)

### The Vulnerability (Unsafe)
We used Python f-strings to construct the query. This is dangerous because user input modifies the query structure.
```python
# BAD PRACTICE
sql_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"