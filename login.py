from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)

# Function to create a sample database with one user
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    # Add a sample user (username: 'testuser', password: 'password123')
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', ('testuser', 'password123'))
    except sqlite3.IntegrityError:
        pass  # Ignore if the user already exists
    conn.commit()
    conn.close()

# Route for the login page
@app.route('/')
def login_form():
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
    </head>
    <body>
        <h2>Login</h2>
        <form action="/login" method="POST">
            <label for="username">Username:</label><br>
            <input type="text" id="username" name="username"><br><br>
            <label for="password">Password:</label><br>
            <input type="password" id="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
        <p>{{ message }}</p>
    </body>
    </html>
    ''')

# Route to handle login submissions
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        return redirect(url_for('welcome', username=username))
    else:
        return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login</title>
        </head>
        <body>
            <h2>Login</h2>
            <form action="/login" method="POST">
                <label for="username">Username:</label><br>
                <input type="text" id="username" name="username"><br><br>
                <label for="password">Password:</label><br>
                <input type="password" id="password" name="password"><br><br>
                <input type="submit" value="Login">
            </form>
            <p style="color:red;">Invalid username or password.</p>
        </body>
        </html>
        ''')

# Welcome page
@app.route('/welcome/<username>')
def welcome(username):
    return f"<h1>Welcome, {username}!</h1>"

if __name__ == '__main__':
    create_db()
    app.run(debug=True)
