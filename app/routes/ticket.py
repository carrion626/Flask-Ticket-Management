from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required
from sqlalchemy import or_, desc

from app import db
from app.decorators import role_required
from data.models import Ticket, User

ticket_bp = Blueprint('ticket', __name__)


@ticket_bp.route('/index')
@login_required
def index():
    """
    Display the list of tickets.

    This view is accessible to all authenticated users. The displayed tickets depend
    on the role of the current user (in descending order):

    - Admin: All tickets are displayed.
    - Non-Admin: Only tickets assigned to the user's group or to the user directly are
      displayed.

    Returns:
        A rendered template showing the list of tickets.
    """
    if current_user.role == 'Admin':
        tickets = Ticket.query.order_by(desc(Ticket.created_at)).all()
    else:
        tickets = Ticket.query.filter(
            or_(
                Ticket.group_id == current_user.group_id,
                Ticket.user_id == current_user.id
            )
        ).order_by(desc(Ticket.created_at)).all()
    return render_template('home.html', tickets=tickets)


@ticket_bp.route('/ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def ticket(id):
    """
    View and update a specific ticket.

    This view is accessible to all authenticated users. It allows viewing and updating
    of a specific ticket's details, including status and note. Admin users can also
    update the assignment of the ticket to a group or user.

    Args:
        id (int): The ID of the ticket to be viewed or updated.

    Returns:
        A rendered template showing the ticket details if accessed via GET.
        A redirect to the ticket index page if accessed via POST after updating the
        ticket details.
    """
    ticket = Ticket.query.get_or_404(id)
    users = User.query.all()
    if request.method == 'POST':
        ticket.status = request.form['status']
        ticket.note = request.form['note']
        if current_user.role == 'Admin':
            assigned = request.form['assigned']
            try:
                group_id = int(assigned)
                ticket.group_id = group_id
                ticket.user_id = None
            except ValueError:
                user = User.query.filter_by(username=assigned).first()
                if user:
                    ticket.user_id = user.id
                    ticket.group_id = None

        db.session.commit()
        return redirect(url_for('ticket.index'))
    return render_template('ticket.html', ticket=ticket, users=users)


@ticket_bp.route('/new_ticket', methods=['GET', 'POST'])
@login_required
@role_required(['Admin', 'Manager'])
def new_ticket():
    """
    Create a new ticket.

    This view is accessible to all authenticated users except users with role 'Analyst'.
    It allows the creation of a new ticket with a note.

    Returns:
        A rendered template showing the form to create a new ticket if accessed via GET.
        A redirect to the ticket index page if accessed via POST after creating the
        new ticket.
    """
    if request.method == 'POST':
        note = request.form['note']
        ticket = Ticket(note=note)
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('ticket.index'))
    return render_template('new_ticket.html')
