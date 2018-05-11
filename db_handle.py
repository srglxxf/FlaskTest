from hello import db, Role, User

db.create_all()

admin_role = Role(name='Admin')
mod_role = Role(name='Moderator')
user_role = Role(name='User')
user_john = User(username='join', role = admin_role)
user_susan = User(username='susan', role = user_role)
user_david = User(username='david', role = user_role)

db.session.add_all([admin_role, mod_role, user_role, user_david, user_john, user_susan])

db.session.commit()

print Role.query.all()
