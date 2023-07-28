
from json import JSONEncoder
import json

class SpaceAssignment():
    user_id = 0
    space_id = 0
 

    def __init__(self, user_id, space_id):
        self.user_id = user_id
        self.space_id = space_id



class SpaceAssignmentJSONEncoder(JSONEncoder):
    def default(self, obj):
        return obj.__dict__



space_assignment = SpaceAssignment(1,1)
json_data = json.dumps(space_assignment, cls=SpaceAssignmentJSONEncoder)
print(json_data)