#!/usr/bin/env python3
"""app module
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask("__name__")
AUTH = Auth()


@app.route('/')
def hello():
    """ return message"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """register user if not exist """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": "<registered email>", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
