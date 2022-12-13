from api import app, db
from api.models.user import UserModel


@app.cli.command('createsuperuser')
def create_superuser():
    """
    Creates a user with the admin role
    """
    username = input("Username[default 'admin']:")
    password = input("Password[default 'admin']:")
    username = 'admin' if not username else username
    password = 'admin' if not password else password
    check_name = UserModel.query.filter(UserModel.username == username)
    if check_name:
        print(f"User with name {username} already exists")
    else:
        user = UserModel(username, password, role="admin")
        user.save()
        print(f"Superuser create successful! id={user.id}")

# TODO доработать и скрипты с бд
