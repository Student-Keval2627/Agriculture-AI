from functools import wraps

from flask import jsonify, session


def get_current_user_id():
    return session.get("user_id")


def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if not get_current_user_id():
            return jsonify({
                "success": False,
                "message": "Please login first"
            }), 401

        return view_function(*args, **kwargs)

    return wrapped_view