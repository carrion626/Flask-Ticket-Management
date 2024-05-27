from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

from app import db
from app.decorators import role_required
from data.models import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/manage_users', methods=['GET', 'POST'])
@login_required
@role_required(['Admin'])
def manage_users():
    """
    Manage user group assignments.

    This view is accessible only to users with the 'Admin' role. It allows them
    to view and update the group assignments of other users (excluding other admins).

    If accessed via GET, the function renders a template showing all non-admin users
    and their current group assignments.

    If accessed via POST, the function updates the group assignments.

    Returns:
        A rendered template for managing users if accessed via GET.
        A redirect to the same page with a success message if accessed via POST.

    Raises:
        A redirect to the ticket index page with a danger message if the current user
        does not have the 'Admin' role.
    """
    users = User.query.filter(User.role != 'Admin').all()
    if request.method == 'POST':
        for user in users:
            group_id = request.form.get(f'group_{user.id}')
            user.group_id = group_id
            db.session.commit()
        flash('User groups updated successfully!', 'success')
        return redirect(url_for('user.manage_users'))
    return render_template('users.html', users=users)
