from urllib.parse import urlparse

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user

from data.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log in a user.

    This view allows users to log in to the application. If the user is already
    authenticated, they are redirected to the index page. If the login attempt
    is unsuccessful, an error message is flashed.

    Returns:
        A rendered login template if accessed via GET.
        A redirect to the index page or the next page after successful login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('ticket.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'warning')
            return redirect(url_for('auth.login'))
        login_user(user, remember=True)
        next_p = request.args.get('next')
        if not next_p or urlparse(next_p).netloc != '':
            next_p = url_for('ticket.index')
        return redirect(next_p)
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    """
    Log out a user.

    This view logs out the currently authenticated user.

    Returns:
        A redirect to the index page after successful logout.
    """
    logout_user()
    return redirect(url_for('ticket.index'))
