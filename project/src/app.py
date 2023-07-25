import sys
sys.path.insert(1, '/workspaces/shared-spaces/project/src/repository')
sys.path.insert(1, '/workspaces/shared-spaces/project/src/exception')
sys.path.insert(1, '/workspaces/shared-spaces/project/src/persistence')

from flask import Flask
from user_repository import create_user
from post_repository import create_post
from space_repository import create_space
from space_assignment_repository import create_space_assignment
from user_repository import get_all_users
from user_repository import get_user_by_email
from repository_exception import RepositoryException


app = Flask(__name__)


try:
    create_user("email@test2.pl")
except RepositoryException as re:
    print(re)

create_post(1, "text 1")
create_space('space 1')
create_space_assignment(1,1)

# for user in get_all_users():
#     print(str(user.user_id) + ' ' + user.email)

user = get_user_by_email("email@test1.pl")
print('find: ')
print(user)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
