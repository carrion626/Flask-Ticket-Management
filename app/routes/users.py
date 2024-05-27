from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

from app import db
from data.models import User

user_bp = Blueprint('user', __name__)


@user_bp.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.role != 'Admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('ticket.index'))
    users = User.query.filter(User.role != 'Admin').all()
    if request.method == 'POST':
        for user in users:
            group_id = request.form.get(f'group_{user.id}')
            user.group_id = group_id
            db.session.commit()
        flash('User groups updated successfully!', 'success')
        return redirect(url_for('user.manage_users'))
    return render_template('users.html', users=users)

