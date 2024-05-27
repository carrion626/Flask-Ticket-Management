from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def role_required(roles):
    """
    Decorator to restrict access based on user role.

    Args:
        roles (list): A list of roles required to access the view.

    Returns:
        Function: Decorated function.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if current_user.role not in roles:
                flash('You do not have access to this page.', 'danger')
                return redirect(url_for('ticket.index'))
            return view_func(*args, **kwargs)
        return wrapper
    return decorator
