#!/usr/bin/env python3
"""app module
"""
from flask import Flask, jsonify, request, abort, redirect, url_for
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """destroy the session and redirect the user to/"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect(url_for("hello"))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def method_name():
    """ find user by session"""
    session_id = request.cookies.get('session_id', None)
    if session_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ reset password"""
    email = request.form.get('email')
    if email is None:
        abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except Exception:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """ update password """
    email = request.form.get("email")
    reset_token = request.form.grt("reset_token")
    new_password = request.form.get("new_password")
    try: 
        AUTH.update_password(reset_token, new_password)
    except Exception:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
