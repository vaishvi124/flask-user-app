from flask import Flask, render_template, request, redirect, url_for
from db_config import get_db_connection

app = Flask(__name__)

# Hello Route
@app.route('/hello')
def hello():
    return "Hello World!"

# Show All Users
@app.route('/users')
def users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template('users.html', users=users)

# Add New User
@app.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, role) VALUES (%s, %s, %s)",
            (name, email, role)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('users'))

    return render_template('new_user.html')

@app.route('/users/<int:id>')
def user_detail(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return render_template('error.html', message="User not found")

    return render_template('user_detail.html', user=user)

# Run Server (ALWAYS LAST)
if __name__ == '__main__':
    app.run(debug=True)

