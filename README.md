# Ticket Management System
Web application in Flask that implements a simple ticket system with different user roles and groups.

Python 3.9.13

# How to install:
- Create directory where you want to store project.
- Write in console "git clone https://github.com/carrion626/Flask-Ticket-Management.git"
- Adjust info in data/template.env 
- Rename "template.env" -> ".env"
- Create new schema for MySQL
- Install requirements
- Run 'create_users.py' to create users (admin, manager1, manager2, analyst) and groups: (Customer 1, 2, 3)
- Run 'run.py'
- Link in console for localhost

# Functionality:
Application has a simple authentication mechanism.
The tickets have the following properties:
1. Status:
   - Pending
   - In review
   - Closed
2. User or Group assignment
3. Note (Simple text field)

Users can be managed by RBAC(Role Based Access Control):
1. Admin
    - Manage all the groups.
2. Manager
   - Has an assignment for a group - can manage only tickets from the assigned group.
3. Analyst
   - Has an assignment for a group - can work only with tickets from the assigned group.
4. Users groups
   - Customer 1
   - Customer 2
   - Customer 3