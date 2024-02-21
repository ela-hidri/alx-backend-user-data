#!/usr/bin/env python3
"""app module
"""
from flask import Flask, jsonify, request, abort, redirect
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
        msg = {"email": email, "message": "user created"}
        return jsonify(msg)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login():
    """ login and create session """
    email = request.form.get("email")
    password = request.form.get("password")
    if AUTH.valid_login(email, password):
        session_Id = AUTH.create_session(email)
        out = jsonify(request.form)
        out.set_cookie("session_id", session_Id)
        return out
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout():
    """destroy the session and redirect the user to/"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    else:
        AUTH.destroy_session(session_id)
        return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
