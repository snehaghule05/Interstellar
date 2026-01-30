from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# -------------------------
# DATABASE CONNECTION
# -------------------------
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # XAMPP default
        password="",          # XAMPP default
        database="interstellar_database"
    )

# -------------------------
# SIGNUP API
# -------------------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    location = data.get("location")

    if not username or not email or not password:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # check if email already exists
    cursor.execute("SELECT user_id FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        return jsonify({"success": False, "message": "Email already registered"}), 409

    # insert new user
    cursor.execute(
        "INSERT INTO users (username, email, password, location) VALUES (%s, %s, %s, %s)",
        (username, email, password, location)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"success": True, "message": "Signup successful"})

# -------------------------
# LOGIN API
# -------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT user_id, username FROM users WHERE email = %s AND password = %s",
        (email, password)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": user
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

# -------------------------
# SERVER RUN
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
