import sqlite3

def sql_to_db(sql_file, db_file):
    # Connect to the SQLite database (creates it if it doesn't exist)
    with sqlite3.connect(db_file) as conn:
        cursor = conn.cursor()

        # Read the SQL file
        with open(sql_file, 'r') as file:
            sql_script = file.read()

        # Execute the SQL commands
        cursor.executescript(sql_script)

def insert_person(cursor, username, email, password, age, tags):
    cursor.execute('''
        INSERT INTO People (username, email, password, age, tags)
        VALUES (?, ?, ?, ?, ?);
    ''', (username, email, password, age, tags))

# Convert SQL to DB
sql_to_db(r'C:\Users\ethan\OneDrive\Desktop\CS Courses\CS201 R&L\userData.sql', 'userData.db')

# Connect to the SQLite database (or create it if it doesn't exist)
with sqlite3.connect('userData.db') as conn:
    cursor = conn.cursor()

    # Create the People table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS People (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            age INTEGER,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            tags TEXT NOT NULL
        );
    ''')

    # Insert example data
    insert_person(cursor, 'john_doe', 'john@example.com', 'hashed_password1', 30, 'developer, tech')
    insert_person(cursor, 'jane_smith', 'jane@example.com', 'hashed_password2', 25, 'designer, art')

    # Commit changes
    conn.commit()

    # Fetch and print all rows
    cursor.execute('SELECT * FROM People;')
    results = cursor.fetchall()
    for row in results:
        print(row)

# No need to explicitly close cursor and connection; 'with' handles it
