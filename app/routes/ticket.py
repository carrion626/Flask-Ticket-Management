from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_required

from sqlalchemy import or_

from app import db
from data.models import Ticket, User

ticket_bp = Blueprint('ticket', __name__)


@ticket_bp.route('/index')
@login_required
def index():
    if current_user.role == 'Admin':
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter(
            or_(
                Ticket.group_id == current_user.group_id,
                Ticket.user_id == current_user.id
            )
        ).all()
    return render_template('home.html', tickets=tickets)


@ticket_bp.route('/ticket/<int:id>', methods=['GET', 'POST'])
@login_required
def ticket(id):
    ticket = Ticket.query.get_or_404(id)
    users = User.query.all()
    if request.method == 'POST':
        ticket.status = request.form['status']
        ticket.note = request.form['note']
        assigned = request.form['assigned']  #  TODO: only for admin

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
def new_ticket():
    if request.method == 'POST':
        note = request.form['note']
        ticket = Ticket(note=note)
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for('ticket.index'))
    return render_template('new_ticket.html')
