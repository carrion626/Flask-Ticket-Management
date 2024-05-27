from app import create_app, db
from data.models import User, Group
from sqlalchemy import text

app = create_app()
with app.app_context():
    with db.engine.connect() as connection:
        connection.execute(text('ALTER TABLE `group` AUTO_INCREMENT = 1'))
        connection.execute(text('ALTER TABLE user AUTO_INCREMENT = 1'))

    db.create_all()

    group1 = Group(name='Customer 1')
    group2 = Group(name='Customer 2')
    group3 = Group(name='Customer 3')

    db.session.add(group1)
    db.session.add(group2)
    db.session.add(group3)
    db.session.commit()

    admin = User(username='admin', email='admin@admin.com', role='Admin')
    admin.set_password('admin')

    manager1 = User(username='manager1', email='manager1@manager.com', role='Manager', group_id=group1.id)
    manager1.set_password('manager1')

    manager2 = User(username='manager2', email='manager2@manager.com', role='Manager', group_id=group1.id)
    manager2.set_password('manager2')

    analyst = User(username='analyst', email='analyst@analyst.com', role='Analyst', group_id=group1.id)
    analyst.set_password('analyst')

    db.session.add(admin)
    db.session.add(manager1)
    db.session.add(manager2)
    db.session.add(analyst)
    db.session.commit()
