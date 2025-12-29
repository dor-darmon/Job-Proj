import sqlite3
from flask import Flask, render_template, request, g

# Configuration
DATABASE = 'demo_database.db'
app = Flask(__name__)
app.secret_key = 'super_secret_key_for_session_management'

# Database Helper Functions
def get_db():
    """Opens a new database connection if one does not exist."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Return rows as dictionaries for easier access
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Closes the database connection at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initializes the database with a users table and a dummy admin account."""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        
        # Check if admin exists, if not, create it
        cursor.execute('SELECT * FROM users WHERE username = "admin"')
        if not cursor.fetchone():
            cursor.execute('INSERT INTO users (username, password) VALUES ("admin", "password123")')
            db.commit()

# Application Routes

@app.route('/')
def home():
    """Renders the main dashboard with both login forms."""
    return render_template('index.html')

@app.route('/login_vulnerable', methods=['POST'])
def login_vulnerable():
    """
    VULNERABLE LOGIN IMPLEMENTATION
    Demonstrates SQL Injection by concatenating user input directly into the query string.
    """
    username = request.form['username']
    password = request.form['password']
    
    db = get_db()
    cursor = db.cursor()

    # VULNERABILITY: Constructing SQL query using f-strings (Direct Concatenation)
    # This allows an attacker to alter the query logic.
    sql_query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    print(f"[VULNERABLE LOG] Executing Query: {sql_query}") # Log to console for educational purposes

    try:
        # execute() allows multiple statements if script injection is used, 
        # but executescript() is needed for that. verify logic here relies on logic bypass.
        cursor.execute(sql_query)
        user = cursor.fetchone()

        if user:
            return render_template('index.html', 
                                   vulnerable_result="SUCCESS: Logged in as " + user['username'], 
                                   vulnerable_color="green")
        else:
            return render_template('index.html', 
                                   vulnerable_result="FAILURE: Invalid credentials", 
                                   vulnerable_color="red")
    except Exception as e:
        return render_template('index.html', 
                               vulnerable_result=f"DATABASE ERROR: {str(e)}", 
                               vulnerable_color="red")

@app.route('/login_secure', methods=['POST'])
def login_secure():
    """
    SECURE LOGIN IMPLEMENTATION
    Uses Parameterized Queries to prevent SQL Injection.
    """
    username = request.form['username']
    password = request.form['password']
    
    db = get_db()
    cursor = db.cursor()

    # MITIGATION: Using placeholders (?)
    # The database driver treats inputs as data, not executable code.
    sql_query = "SELECT * FROM users WHERE username = ? AND password = ?"
    
    print(f"[SECURE LOG] Executing Query: {sql_query} with params ({username}, {password})")

    cursor.execute(sql_query, (username, password))
    user = cursor.fetchone()

    if user:
        return render_template('index.html', 
                               secure_result="SUCCESS: Logged in as " + user['username'], 
                               secure_color="green")
    else:
        return render_template('index.html', 
                               secure_result="FAILURE: Attack neutralized (Invalid credentials)", 
                               secure_color="green")

# Main Entry Point

if __name__ == '__main__':
    # Initialize the DB before running
    init_db()
    print("System: Database initialized. Admin user created (User: admin, Pass: password123)")
    app.run(debug=True, port=5002)