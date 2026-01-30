from flask import Flask, request, jsonify
from flask_cors import CORS
from login_logic import register_user, login_user, sessions

import mysql.connector

app = Flask(__name__)
CORS(app)

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

  data = request.json
    msg = register_user(username,email,password,location)
    if user:
        return jsonify({
            "success": True,
            "message": "Sign-in successful",
            "user": user
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

# -------------------------
# LOGIN API
# -------------------------
@app.route("/login", methods=["POST"])
def login():
   data = request.json
    result = login_user(email,password)
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
