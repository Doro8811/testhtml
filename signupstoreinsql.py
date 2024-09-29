from flask import Flask, request, render_template
import sqlite3

app = Flask(__name__)

# Create the database and table (if not already created)
def init_db():
    conn = sqlite3.connect('form_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Route for displaying the form
@app.route('/')
def form():
    return render_template('form.html')

# Route for processing the form submission and storing in SQLite
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')

    # Store the form data in SQLite database
    conn = sqlite3.connect('form_data.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
    conn.commit()
    conn.close()

    return f"Received: Name = {name}, Email = {email}, stored in SQLite DB!"

if __name__ == '__main__':
    init_db()  # Initialize the database and table on startup
    app.run(debug=True)
