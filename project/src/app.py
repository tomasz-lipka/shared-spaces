from flask import Flask
from user_repository import create_user
from user_repository import get_all_users
from user_repository import find_user_by_email


app = Flask(__name__)

# create_user("email@test2.pl")

for user in get_all_users():
    print(str(user.user_id) + ' ' + user.email)


for user in find_user_by_email("email@test2.pl"):
    print(str(user.user_id) + ' ' + user.email)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
